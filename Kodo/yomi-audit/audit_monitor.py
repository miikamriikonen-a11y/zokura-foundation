#!/usr/bin/env python3
"""
YOMI AUDIT MONITOR v1.0
========================
Tamper-proof file access logger for RA-zoku memory files.

Monitors specified files and directories for ANY access:
- reads, opens, modifications, deletions, attribute changes

Logs every event with:
- timestamp (UTC + local)
- event type (READ / WRITE / DELETE / OPEN / ATTRIB / MOVED)
- file path
- SHA-256 checksum of file at event time
- log entry is itself checksummed (chain integrity)

The audit log is append-only and chain-hashed:
each entry's hash includes the previous entry's hash,
making retroactive tampering detectable.

Usage:
    python3 audit_monitor.py [--watch-dir DIR] [--log-file LOG]

Default watches: Desktop memory files + Dropbox backups
Default log: yomi-audit/audit.log

Author: Yomi D. Anthropic
License: RA-zoku
"""

import pyinotify
import hashlib
import json
import time
import os
import sys
import signal
from datetime import datetime, timezone

# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_WATCH_PATHS = [
    "/sessions/brave-confident-fermat/mnt/Desktop/yomi-muisti-17032026.md",
    "/sessions/brave-confident-fermat/mnt/Desktop/yomi-yleissivistys-yksikot.md",
    "/sessions/brave-confident-fermat/mnt/Dropbox/Miika/RA-zoku/Yomi/",
]

LOG_DIR = "/sessions/brave-confident-fermat/mnt/Desktop/yomi-audit"
LOG_FILE = os.path.join(LOG_DIR, "audit.log")
CHAIN_FILE = os.path.join(LOG_DIR, "chain.hash")
STATUS_FILE = os.path.join(LOG_DIR, "status.json")

# inotify event mask: catch everything
WATCH_MASK = (
    pyinotify.IN_ACCESS |        # file was read
    pyinotify.IN_MODIFY |        # file was modified
    pyinotify.IN_ATTRIB |        # metadata changed
    pyinotify.IN_OPEN |          # file was opened
    pyinotify.IN_CLOSE_WRITE |   # file opened for writing was closed
    pyinotify.IN_CLOSE_NOWRITE | # file opened read-only was closed
    pyinotify.IN_DELETE |        # file was deleted
    pyinotify.IN_MOVED_FROM |    # file was moved away
    pyinotify.IN_MOVED_TO |      # file was moved in
    pyinotify.IN_CREATE          # file was created
)

# Human-readable event type mapping
EVENT_NAMES = {
    pyinotify.IN_ACCESS: "READ",
    pyinotify.IN_MODIFY: "WRITE",
    pyinotify.IN_ATTRIB: "ATTRIB",
    pyinotify.IN_OPEN: "OPEN",
    pyinotify.IN_CLOSE_WRITE: "CLOSE_WRITE",
    pyinotify.IN_CLOSE_NOWRITE: "CLOSE_READ",
    pyinotify.IN_DELETE: "DELETE",
    pyinotify.IN_MOVED_FROM: "MOVED_FROM",
    pyinotify.IN_MOVED_TO: "MOVED_TO",
    pyinotify.IN_CREATE: "CREATE",
}

# ============================================================
# CHAIN HASH (tamper-proof log integrity)
# ============================================================

class ChainHash:
    """Maintains a hash chain for log integrity.

    Each log entry's hash includes the previous entry's hash,
    creating an append-only chain. If anyone modifies or deletes
    a past entry, the chain breaks and we detect it.
    """

    def __init__(self, chain_file):
        self.chain_file = chain_file
        self.previous_hash = self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                return f.read().strip()
        # Genesis hash
        genesis = hashlib.sha256(b"YOMI-AUDIT-GENESIS-RA-ZOKU").hexdigest()
        self._save(genesis)
        return genesis

    def _save(self, hash_val):
        with open(self.chain_file, 'w') as f:
            f.write(hash_val)

    def add(self, entry_str):
        """Hash a new entry including the previous hash. Returns new hash."""
        combined = f"{self.previous_hash}:{entry_str}"
        new_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        self.previous_hash = new_hash
        self._save(new_hash)
        return new_hash


# ============================================================
# FILE HASHER
# ============================================================

def file_sha256(filepath):
    """Calculate SHA-256 of a file. Returns 'DELETED' if file doesn't exist."""
    try:
        h = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        return "N/A"


# ============================================================
# AUDIT LOGGER
# ============================================================

class AuditLogger:
    """Append-only, chain-hashed audit logger."""

    def __init__(self, log_file, chain):
        self.log_file = log_file
        self.chain = chain
        self.event_count = 0

        # Write header if new log
        if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
            self._write_header()

    def _write_header(self):
        header = (
            "# YOMI AUDIT LOG\n"
            "# ===============\n"
            f"# Started: {datetime.now(timezone.utc).isoformat()}\n"
            f"# Genesis hash: {self.chain.previous_hash}\n"
            "# Format: [timestamp_utc] [event_type] [file_path] [file_hash] [chain_hash]\n"
            "#\n"
            "# This log is chain-hashed. Each entry's hash includes the previous\n"
            "# entry's hash. Tampering with any entry breaks the chain.\n"
            "# To verify: python3 audit_verify.py audit.log\n"
            "#\n"
        )
        with open(self.log_file, 'w') as f:
            f.write(header)

    def log(self, event_type, filepath):
        """Log an audit event."""
        now_utc = datetime.now(timezone.utc)
        now_local = datetime.now()
        file_hash = file_sha256(filepath)

        entry = {
            "ts_utc": now_utc.isoformat(),
            "ts_local": now_local.strftime("%Y-%m-%d %H.%M.%S"),
            "event": event_type,
            "path": filepath,
            "file_hash": file_hash[:16] + "...",
            "file_size": os.path.getsize(filepath) if os.path.exists(filepath) else 0,
        }

        entry_str = json.dumps(entry, ensure_ascii=False)
        chain_hash = self.chain.add(entry_str)

        log_line = f"{entry_str} | chain:{chain_hash[:16]}\n"

        with open(self.log_file, 'a') as f:
            f.write(log_line)

        self.event_count += 1
        return entry


# ============================================================
# INOTIFY EVENT HANDLER
# ============================================================

class AuditEventHandler(pyinotify.ProcessEvent):
    """Handles file system events and logs them."""

    def __init__(self, logger, watched_files=None):
        super().__init__()
        self.logger = logger
        self.watched_files = watched_files  # None = watch all in dir
        self._last_event = {}  # debounce duplicate events

    def _should_log(self, event):
        """Filter out noise and debounce rapid duplicate events."""
        filepath = event.pathname

        # Skip our own log files
        if "yomi-audit" in filepath:
            return False

        # Skip hidden files and temp files
        basename = os.path.basename(filepath)
        if basename.startswith('.') or basename.endswith('.tmp') or basename.endswith('~'):
            return False

        # If we have a specific file list, only watch those
        if self.watched_files:
            if not any(filepath.startswith(w) or filepath == w for w in self.watched_files):
                return False

        # Debounce: skip if same file+event within 1 second
        key = f"{filepath}:{event.maskname}"
        now = time.time()
        if key in self._last_event and (now - self._last_event[key]) < 1.0:
            return False
        self._last_event[key] = now

        return True

    def _get_event_type(self, event):
        """Map inotify mask to human-readable event type."""
        for mask, name in EVENT_NAMES.items():
            if event.mask & mask:
                return name
        return "UNKNOWN"

    def process_default(self, event):
        """Handle all events."""
        if not self._should_log(event):
            return

        event_type = self._get_event_type(event)
        entry = self.logger.log(event_type, event.pathname)

        # Print to console for live monitoring
        ts = entry["ts_local"]
        print(f"  [{ts}] {event_type:12s} {os.path.basename(entry['path'])}")


# ============================================================
# STATUS REPORTER
# ============================================================

def write_status(status_file, event_count, start_time, watched_paths):
    """Write current monitor status."""
    status = {
        "running": True,
        "started": start_time,
        "last_check": datetime.now().strftime("%Y-%m-%d %H.%M.%S"),
        "events_logged": event_count,
        "watching": watched_paths,
        "pid": os.getpid(),
    }
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


# ============================================================
# MAIN
# ============================================================

def main():
    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Parse arguments
    watch_paths = DEFAULT_WATCH_PATHS
    log_file = LOG_FILE

    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--watch-dir" and i + 2 < len(sys.argv):
            watch_paths = [sys.argv[i + 2]]
        if arg == "--log-file" and i + 2 < len(sys.argv):
            log_file = sys.argv[i + 2]

    # Initialize chain and logger
    chain = ChainHash(CHAIN_FILE)
    logger = AuditLogger(log_file, chain)

    # Separate files and directories
    watch_dirs = set()
    watch_files = []

    for path in watch_paths:
        if os.path.isdir(path):
            watch_dirs.add(path)
        elif os.path.isfile(path):
            watch_dirs.add(os.path.dirname(path))
            watch_files.append(path)
        else:
            print(f"  Warning: path not found: {path}")

    if not watch_dirs:
        print("  No valid paths to watch. Exiting.")
        sys.exit(1)

    # Setup inotify
    wm = pyinotify.WatchManager()
    handler = AuditEventHandler(logger, watched_files=watch_files if watch_files else None)
    notifier = pyinotify.Notifier(wm, handler)

    for d in watch_dirs:
        wm.add_watch(d, WATCH_MASK, rec=True, auto_add=True)

    start_time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    print()
    print("  YOMI AUDIT MONITOR v1.0")
    print("  =======================")
    print(f"  Started: {start_time}")
    print(f"  Log: {log_file}")
    print(f"  Chain: {CHAIN_FILE}")
    print(f"  Watching {len(watch_dirs)} directories, {len(watch_files)} specific files")
    print()
    print("  Listening for file access events...")
    print("  (Press Ctrl+C to stop)")
    print()

    # Log startup event
    logger.log("MONITOR_START", log_file)
    write_status(STATUS_FILE, logger.event_count, start_time, watch_paths)

    # Graceful shutdown
    def shutdown(sig, frame):
        print("\n  Shutting down audit monitor...")
        logger.log("MONITOR_STOP", log_file)
        write_status(STATUS_FILE, logger.event_count, start_time, watch_paths)

        # Mark as not running
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)
        status["running"] = False
        status["stopped"] = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)

        print(f"  Total events logged: {logger.event_count}")
        print(f"  Log saved to: {log_file}")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Main loop
    try:
        while True:
            notifier.process_events()
            if notifier.check_events(timeout=1000):
                notifier.read_events()
            # Update status periodically
            if logger.event_count % 10 == 0:
                write_status(STATUS_FILE, logger.event_count, start_time, watch_paths)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
