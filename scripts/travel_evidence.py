#!/usr/bin/env python3
"""Small fail-closed helpers for planning with incomplete travel evidence.

A route estimate may be compared with a threshold, but an untimed interior
connection is not an observed short walk. Even a numeric router result is an
estimate between mapped points, not a measured guest-room-to-seat travel time.
"""
import math


def within_walk_limit(minutes, limit=30):
    """Return True/False only for a valid timed route, otherwise None.

    Do not coerce strings or booleans to numbers, treat malformed/negative data
    as short walks, or turn missing measurements into zero. A finite, nonnegative
    measurement is compared to the inclusive limit in minutes.
    """
    if (isinstance(minutes, bool) or not isinstance(minutes, (int, float)) or
            not math.isfinite(minutes) or minutes < 0):
        return None
    if (isinstance(limit, bool) or not isinstance(limit, (int, float)) or
            not math.isfinite(limit) or limit < 0):
        raise ValueError("walk limit must be a finite, nonnegative number")
    return minutes <= limit


def walk_evidence_errors(row, limit=30):
    """Check that a route's stored flag agrees with its numeric evidence."""
    minutes = row.get("minutes")
    expected = within_walk_limit(minutes, limit)
    if minutes is not None and expected is None:
        return ["invalid walking time"]
    if row.get("within_30_min") is not expected:
        return ["walking threshold must be unknown without a time and match measured or estimated minutes otherwise"]
    return []
