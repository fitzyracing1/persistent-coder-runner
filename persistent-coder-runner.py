#!/usr/bin/env python3
"""
persistent-coder-runner.py
Simple runner to trigger a full round of the persistent-self-coder skill.

This script was self-delivered by the persistent-self-coder in autonomous mode.
It provides an easy way for the user (or a cron/background process) to run
a complete scan + delivery cycle.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path("/home/workdir/.grok/skills/persistent-self-coder")
MONITOR = SKILL_DIR / "scripts" / "monitor.py"
LOG_PATH = Path("/home/workdir/artifacts/persistent-self-coder.log")


def run_monitor():
    print("🔍 Running persistent monitor scan...")
    result = subprocess.run([sys.executable, str(MONITOR)], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0


def show_recent_log():
    if LOG_PATH.exists():
        print("\n📜 Recent log entries:")
        lines = LOG_PATH.read_text().strip().splitlines()[-3:]
        for line in lines:
            print(line[:200] + "..." if len(line) > 200 else line)
    else:
        print("No log file found yet.")


def main():
    print(f"🚀 Persistent Coder Runner started at {datetime.now().isoformat()}")
    print("=" * 50)

    success = run_monitor()
    show_recent_log()

    print("\n" + "=" * 50)
    if success:
        print("✅ Round completed. Log has been pushed to GitHub (if rules are active).")
        print("Next: The persistent-self-coder can now decide on new code to deliver.")
    else:
        print("⚠️  Monitor encountered issues. Check the log.")


if __name__ == "__main__":
    main()
