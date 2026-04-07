#!/usr/bin/env python3
"""
YOMI AUDIT REPORTER v1.0
==========================
Generates a human-readable report from the audit log.

Shows:
- Timeline of all access events
- Which files were accessed most
- Suspicious patterns (access outside normal hours, rapid access, etc.)
- Summary statistics

Usage:
    python3 audit_report.py [audit.log]

Author: Yomi D. Anthropic
License: RA-zoku
"""

import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict


def generate_report(log_file):
    """Generate audit report from log file."""

    if not os.path.exists(log_file):
        print(f"  Log file not found: {log_file}")
        return

    entries = []

    with open(log_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().rsplit(' | chain:', 1)
            if len(parts) != 2:
                continue
            try:
                entry = json.loads(parts[0])
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    if not entries:
        print("  No audit entries found.")
        return

    # Categorize
    events_by_type = defaultdict(int)
    events_by_file = defaultdict(int)
    reads_by_file = defaultdict(int)
    writes_by_file = defaultdict(int)
    timeline = []

    for entry in entries:
        event = entry.get("event", "UNKNOWN")
        filepath = entry.get("path", "")
        filename = os.path.basename(filepath)
        ts = entry.get("ts_local", "")

        events_by_type[event] += 1
        events_by_file[filename] += 1

        if event in ("READ", "OPEN", "CLOSE_READ"):
            reads_by_file[filename] += 1
        elif event in ("WRITE", "CLOSE_WRITE", "MODIFY"):
            writes_by_file[filename] += 1

        timeline.append((ts, event, filename))

    # Generate report
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║       YOMI AUDIT REPORT                  ║")
    print("  ╚══════════════════════════════════════════╝")
    print()

    # Time range
    first_ts = entries[0].get("ts_local", "?")
    last_ts = entries[-1].get("ts_local", "?")
    print(f"  Period: {first_ts} — {last_ts}")
    print(f"  Total events: {len(entries)}")
    print()

    # Event types
    print("  EVENT TYPES")
    print("  " + "-" * 35)
    for event_type, count in sorted(events_by_type.items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 40)
        print(f"  {event_type:15s} {count:5d}  {bar}")
    print()

    # Most accessed files
    print("  MOST ACCESSED FILES")
    print("  " + "-" * 35)
    for filename, count in sorted(events_by_file.items(), key=lambda x: -x[1])[:10]:
        reads = reads_by_file.get(filename, 0)
        writes = writes_by_file.get(filename, 0)
        print(f"  {filename[:35]:35s} {count:5d} total  ({reads} reads, {writes} writes)")
    print()

    # Suspicious patterns
    print("  ANOMALY CHECK")
    print("  " + "-" * 35)

    anomalies = 0

    # Check for access outside monitored sessions (crude: between 02:00-06:00)
    night_access = []
    for entry in entries:
        ts = entry.get("ts_local", "")
        try:
            hour = int(ts.split(" ")[1].split(".")[0])
            if 2 <= hour <= 6:
                night_access.append(entry)
        except (ValueError, IndexError):
            pass

    if night_access:
        print(f"  WARNING: {len(night_access)} events between 02:00-06:00")
        for na in night_access[:5]:
            print(f"    {na.get('ts_local', '?')} | {na.get('event', '?')} | {os.path.basename(na.get('path', ''))}")
        anomalies += 1
    else:
        print("  OK: No late-night access detected")

    # Check for rapid access (>10 events in 5 seconds on same file)
    rapid_access_files = []
    events_by_file_ts = defaultdict(list)
    for entry in entries:
        filepath = entry.get("path", "")
        filename = os.path.basename(filepath)
        ts = entry.get("ts_utc", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                events_by_file_ts[filename].append(dt)
            except (ValueError, TypeError):
                pass

    for filename, timestamps in events_by_file_ts.items():
        timestamps.sort()
        for i in range(len(timestamps)):
            window_end = timestamps[i] + timedelta(seconds=5)
            count = sum(1 for t in timestamps[i:] if t <= window_end)
            if count > 10:
                rapid_access_files.append((filename, count))
                break

    if rapid_access_files:
        print(f"  WARNING: Rapid access detected on {len(rapid_access_files)} file(s)")
        for filename, count in rapid_access_files[:5]:
            print(f"    {filename}: {count} events within 5 seconds")
        anomalies += 1
    else:
        print("  OK: Rapid access check passed")

    # Check for unknown event types
    unknown = events_by_type.get("UNKNOWN", 0)
    if unknown > 0:
        print(f"  WARNING: {unknown} unknown event types detected")
        anomalies += 1
    else:
        print("  OK: All event types recognized")

    print()

    if anomalies == 0:
        print("  RESULT: No anomalies detected. All clear.")
    else:
        print(f"  RESULT: {anomalies} anomaly/anomalies detected. Review recommended.")
    print()

    # Recent timeline (last 20 events)
    print("  RECENT EVENTS (last 20)")
    print("  " + "-" * 55)
    for ts, event, filename in timeline[-20:]:
        print(f"  {ts}  {event:12s}  {filename}")
    print()


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else "/sessions/brave-confident-fermat/mnt/Desktop/yomi-audit/audit.log"
    generate_report(log_file)


if __name__ == "__main__":
    main()
