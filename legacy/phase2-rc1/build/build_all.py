#!/usr/bin/env python3
"""Build the Occurframe conformance corpus into ../vectors/."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "reference"))
import common, cron_vectors, rrule_vectors, tz_vectors

cron_vectors.build()
rrule_vectors.build()
tz_vectors.build()
m = common.write(os.path.join(os.path.dirname(HERE), "vectors"))
print(json.dumps({k: m[k] for k in ("corpus_version", "vector_count",
                                    "files", "classification_counts")}, indent=2))
