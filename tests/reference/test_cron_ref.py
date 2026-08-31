import datetime as dt
import importlib.util
import pathlib
import sys
import unittest
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("cron_ref", ROOT / "reference" / "cron_ref.py")
cron_ref = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = cron_ref
SPEC.loader.exec_module(cron_ref)


class CronReferenceCases(unittest.TestCase):
    def zone(self, name):
        try:
            return ZoneInfo(name)
        except ZoneInfoNotFoundError:
            self.skipTest(f"runtime has no IANA zoneinfo payload for {name}")

    def test_sunday_zero_and_seven_are_equivalent_in_vixie_policy(self):
        start = dt.datetime(2026, 1, 1)
        policy = cron_ref.Policy(dow_zero_seven="both")
        self.assertEqual(
            cron_ref.run("0 12 * * 0", policy, start, 3),
            cron_ref.run("0 12 * * 7", policy, start, 3),
        )

    def test_friday_the_thirteenth_uses_vixie_union(self):
        result = cron_ref.run(
            "0 12 13 * FRI",
            cron_ref.Policy(dom_dow="vixie"),
            dt.datetime(2026, 1, 1),
            4,
        )
        self.assertEqual(
            result,
            [
                "2026-01-02T12:00:00",
                "2026-01-09T12:00:00",
                "2026-01-13T12:00:00",
                "2026-01-16T12:00:00",
            ],
        )

    def test_invalid_zero_step_is_rejected(self):
        with self.assertRaises(cron_ref.CronRefError):
            cron_ref.parse("*/0 * * * *", cron_ref.Policy())

    def test_gap_start_and_pre_gap_offset_are_distinct(self):
        start = dt.datetime(2026, 3, 7)
        gap_start = cron_ref.run(
            "30 2 * * *",
            cron_ref.Policy(dst_gap="fire_at_gap_start"),
            start,
            4,
            tz=self.zone("America/New_York"),
        )
        pre_gap_offset = cron_ref.run(
            "30 2 * * *",
            cron_ref.Policy(dst_gap="pre_gap_offset"),
            start,
            4,
            tz=self.zone("America/New_York"),
        )
        self.assertEqual(gap_start[1], "2026-03-08T03:00:00-04:00|2026-03-08T07:00:00Z")
        self.assertEqual(pre_gap_offset[1], "2026-03-08T03:30:00-04:00|2026-03-08T07:30:00Z")

    def test_london_weekly_gap_policy_answers(self):
        start = dt.datetime(2026, 3, 1)
        zone = self.zone("Europe/London")
        skip = cron_ref.run("30 1 * * SUN", cron_ref.Policy(dst_gap="skip"), start, 5, tz=zone)
        next_valid = cron_ref.run("30 1 * * SUN", cron_ref.Policy(dst_gap="next_valid"), start, 5, tz=zone)
        pre_gap_offset = cron_ref.run("30 1 * * SUN", cron_ref.Policy(dst_gap="pre_gap_offset"), start, 5, tz=zone)
        self.assertEqual(skip[-1], "2026-04-05T01:30:00+01:00|2026-04-05T00:30:00Z")
        self.assertEqual(next_valid[-1], "2026-03-29T02:00:00+01:00|2026-03-29T01:00:00Z")
        self.assertEqual(pre_gap_offset[-1], "2026-03-29T02:30:00+01:00|2026-03-29T01:30:00Z")


if __name__ == "__main__":
    unittest.main()
