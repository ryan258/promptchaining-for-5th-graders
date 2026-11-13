"""Inspect model rubric results for a chain and a single-prompt baseline."""

import argparse
from pathlib import Path
import sys
from uuid import uuid4

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from lib.core.errors import user_error
from lib.enhancements.emergence_measurement import batch_measure, generate_report, measure_emergence
from lib.enhancements.natural_reasoning import scientific_method


BATCH_TOPICS = [
    "What would show that a structured intake form reduces missing details?",
    "What would show that an onboarding checklist reduces repeated questions?",
    "What would show that a handoff template helps people resume work?",
    "What would show that spaced practice improves recall for this lesson?",
    "What would show that a weekly office hour helps clear blocked work?",
]
LIMITS = {2: 7, 3: 7, 4: 35, 5: 49}


def explain_metrics():
    print("The judge model scores excerpts on novelty, depth, coherence, pedagogy and actionability.")
    print("These scores express the model’s assessment. They establish neither factual accuracy nor statistical significance.")


def compare(topic):
    result, _ = measure_emergence(topic, scientific_method)
    print(result["analysis"])
    if result["status"] != "completed":
        print("Incomplete comparison. Check provider usage before trying again.")
        return False
    print(f"Model assessment: {result['winner']}")
    print("The judge saw only the configured excerpts.")
    return True


def run_batch():
    aggregate, results = batch_measure(BATCH_TOPICS, scientific_method)
    print(aggregate["conclusion"])
    print(aggregate["statistical_significance"])
    output = project_root / "output" / "emergence" / f"assessment-{uuid4().hex}.md"
    print(f"Report: {generate_report(aggregate, results, str(output))}")
    return aggregate["failed_comparisons"] == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", type=int, choices=[1, 2, 3, 4, 5], default=1,
                        help="1=Rubric, 2=Single, 3=Another single, 4=Batch, 5=All")
    parser.add_argument("--live", action="store_true", help="Send the selected provider requests.")
    args = parser.parse_args(argv)
    if args.demo == 1:
        explain_metrics()
        return 0
    if not args.live:
        parser.error(f"This demo can send up to {LIMITS[args.demo]} provider requests. Pass --live to run it deliberately.")
    print(f"Up to {LIMITS[args.demo]} provider requests. Provider charges apply.")
    try:
        if args.demo in {2, 3}:
            succeeded = compare(BATCH_TOPICS[args.demo - 2])
        elif args.demo == 4:
            succeeded = run_batch()
        else:
            explain_metrics()
            succeeded = compare(BATCH_TOPICS[0]) and compare(BATCH_TOPICS[1]) and run_batch()
    except Exception as exc:
        print(user_error(exc), file=sys.stderr)
        return 1
    return 0 if succeeded else 1


if __name__ == "__main__":
    raise SystemExit(main())
