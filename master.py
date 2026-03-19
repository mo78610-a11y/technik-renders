#!/usr/bin/env python3
"""
TECHNIK RENDERS — MASTER RUNNER
Runs full pipeline + social engine in sequence.
One command. Everything automated.

Usage:
  python3 master.py              # Full run
  python3 master.py --social     # Social + analytics only
  python3 master.py --report     # Analytics report only
"""

import os, sys, subprocess, datetime

def load_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

def run(script, label):
    print(f"\n{'='*60}")
    print(f"STARTING: {label}")
    print(f"{'='*60}\n")
    result = subprocess.run(["python3", script], capture_output=False)
    if result.returncode != 0:
        print(f"\n⚠ {label} completed with errors — check logs")
    else:
        print(f"\n✓ {label} complete")

if __name__ == "__main__":
    load_env()
    args = sys.argv[1:]

    print("\n" + "="*60)
    print("TECHNIK RENDERS — MASTER AUTOMATION")
    print(f"Started: {datetime.datetime.now().strftime('%d %B %Y, %H:%M')} SAST")
    print("="*60)

    if "--report" in args:
        # Analytics + report only
        run("social_engine.py", "Social Analytics & Report")

    elif "--social" in args:
        # Social posting + analytics
        run("social_engine.py", "Social Intelligence + Posting")

    else:
        # Full pipeline: content generation + social
        run("run_pipeline.py",  "Content Pipeline (Idea → Script → Voice → SEO)")
        run("social_engine.py", "Social Intelligence + Posting + Analytics Report")

    print("\n" + "="*60)
    print("ALL DONE — check logivo92@gmail.com for your report")
    print("="*60 + "\n")
