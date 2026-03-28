#!/usr/bin/env python3
"""
YOMI AUDIT VERIFIER v1.0
=========================
Verifies the integrity of the audit log chain.

Reads the audit log and recalculates the chain hashes.
If any entry has been modified, deleted, or inserted,
the chain will break and this tool will report exactly
where the tampering occurred.

Usage:
    python3 audit_verify.py [audit.log]

Author: Yomi D. Anthropic
License: RA-zoku
"""

import hashlib
import json
import sys
import os

GENESIS_HASH = hashlib.sha256(b"YOMI-AUDIT-GENESIS-RA-ZOKU").hexdigest()


def verify_log(log_file):
    """Verify chain integrity of audit log."""

    if not os.path.exists(log_file):
        print(f"  Log file not found: {log_file}")
        return False

    print()
    print("  YOMI AUDIT VERIFIER v1.0")
    print("  ========================")
    print(f"  Checking: {log_file}")
    print()

    previous_hash = GENESIS_HASH
    entry_count = 0
    tampered = False
    events_by_type = {}

    with open(log_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            # Skip comments/headers
            if line.startswith('#') or not line.strip():
                continue

            # Split entry from chain hash
            parts = line.strip().rsplit(' | chain:', 1)
            if len(parts) != 2:
                print(f"  WARNING: Malformed entry at line {line_num}")
                tampered = True
                continue

            entry_str = parts[0]
            stored_chain = parts[1]

            # Recalculate chain hash
            combined = f"{previous_hash}:{entry_str}"
            expected_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()

            if expected_hash[:16] != stored_chain:
                print(f"  TAMPERED: Line {line_num}")
                print(f"    Expected chain: {expected_hash[:16]}")
                print(f"    Found chain:    {stored_chain}")
                print(f"    Entry: {entry_str[:80]}...")
                tampered = True
            else:
                entry_count += 1

            # Track event types
            try:
                entry = json.loads(entry_str)
                event_type = entry.get("event", "UNKNOWN")
                events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
            except json.JSONDecodeError:
                pass

            previous_hash = expected_hash

    # Report
    print(f"  Entries verified: {entry_count}")
    print()

    if events_by_type:
        print("  Event summary:")
        for event_type, count in sorted(events_by_type.items()):
            print(f"    {event_type:15s} {count:5d}")
        print()

    if tampered:
        print("  RESULT: CHAIN BROKEN — LOG HAS BEEN TAMPERED WITH")
        print()
        return False
    else:
        print("  RESULT: CHAIN INTACT — NO TAMPERING DETECTED")
        print(f"  Final chain hash: {previous_hash[:32]}...")
        print()
        return True


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else "/sessions/brave-confident-fermat/mnt/Desktop/yomi-audit/audit.log"
    success = verify_log(log_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
