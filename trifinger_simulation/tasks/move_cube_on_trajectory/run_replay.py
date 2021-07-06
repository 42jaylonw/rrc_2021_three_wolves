#!/usr/bin/env python3
"""Replay results of ``run_evaluate_policy()`` and compute reward.

Reads the files generated by :func:`run_evaluate_policy.run_evaluate_policy`
and replays the action logs to verify the result and to compute the total
reward over all runs.
"""

# IMPORTANT:  DO NOT MODIFY THIS FILE!
# Submissions will be evaluate on our side with our own version of this script.
# To make sure that your code is compatible with our evaluation script, make
# sure it runs with this one without any modifications.

import argparse
import json
import pathlib
import pickle
import sys

import numpy as np

from . import replay_action_log


def add_arguments(parser):
    parser.add_argument(
        "log_directory",
        type=pathlib.Path,
        help="Directory containing the generated log files.",
    )


def main(log_directory: pathlib.Path):
    try:
        if not log_directory.is_dir():
            print(
                "'{}' does not exist or is not a directory.".format(
                    log_directory
                )
            )
            sys.exit(1)

        logfile_tmpl = str(log_directory / "action_log_{:02d}.p")

        # load samples
        sample_file = log_directory / "test_data.p"
        with open(sample_file, "rb") as fh:
            test_data = pickle.load(fh)

        # run "replay_action_log.py" for each sample
        rewards = []
        for i, sample_json in enumerate(test_data):
            print("\n___Replay trajectory {}___".format(i))
            sample = json.loads(sample_json)
            reward = replay_action_log.replay_action_log(
                logfile_tmpl.format(i), sample
            )
            rewards.append(reward)

        # report
        print("\n=======================================================\n")

        report = {
            "mean": np.mean(rewards),
            "median": np.median(rewards),
            "std": np.std(rewards),
        }
        print(
            "reward median: {:.3f},\tmean: {:.3f},\tstd: {:.3f}\n".format(
                report["median"], report["mean"], report["std"]
            )
        )

        # save report to file
        report_file = log_directory / "reward.json"
        with open(report_file, "w") as f:
            json.dump(report, f)

    except Exception as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    main(args.log_directory)
