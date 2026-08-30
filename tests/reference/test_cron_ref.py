import datetime as dt
import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("cron_ref", ROOT / "reference" / "cron_ref.py")
cron_ref = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = cron_ref
SPEC.loader.exec_module(cron_ref)


class CronReferenceCases(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
