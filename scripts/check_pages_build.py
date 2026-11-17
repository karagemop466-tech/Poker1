#!/usr/bin/env python3
"""Read the Pages build state for one commit from the GitHub API.

Reads the JSON array returned by ``GET /repos/{owner}/{repo}/pages/builds`` on stdin and prints
``state|detail`` for the build of the given commit:

    built|            the branch build for this commit succeeded
    errored|<reason>  the branch build for this commit failed
    superseded|<why>  a newer commit superseded this build before it finished; not a failure here
    pending|          no verdict yet

A build that was cancelled or errored only because a newer commit's build replaced it is reported as
``superseded``, because the site then publishes that newer commit.

    python3 scripts/check_pages_build.py <commit-sha> < pages_builds.json
"""
import json
import sys


def verdict(builds, sha):
    sha = (sha or "").strip().lower()
    mine = None
    newer_succeeded = None
    for build in builds:
        commit = (build.get("commit") or "").lower()
        same = bool(commit) and (commit == sha or commit.startswith(sha) or sha.startswith(commit))
        if same and mine is None:
            mine = build
        if not same and build.get("status") == "built":
            created = build.get("created_at") or ""
            if newer_succeeded is None or created > newer_succeeded:
                newer_succeeded = created
    if mine is None:
        return "pending", "no build recorded for this commit yet"
    status = mine.get("status")
    error = ((mine.get("error") or {}).get("message") or "").strip()
    created = mine.get("created_at") or ""
    if status == "built":
        return "built", "%s" % created
    if status == "errored":
        superseded = newer_succeeded is not None and newer_succeeded > created
        if superseded or "cancel" in error.lower():
            return "superseded", "a newer commit published the site at %s" % newer_succeeded
        return "errored", error or "Page build failed."
    return "pending", "%s" % (status or "unknown")


def main(argv):
    if len(argv) != 2:
        print("usage: check_pages_build.py <commit-sha> < pages_builds.json", file=sys.stderr)
        return 2
    try:
        builds = json.load(sys.stdin)
    except ValueError as exc:
        print("could not parse the Pages builds response: %s" % exc, file=sys.stderr)
        return 2
    if not isinstance(builds, list):
        builds = []
    state, detail = verdict(builds, argv[1])
    print("%s|%s" % (state, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
