#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/ttt/.openclaw/workspace/cabbageclaw_paper_daily"
LOG="/home/ttt/.openclaw/workspace/memory/paper-daily-email-cron.log"
today="$(TZ=America/Los_Angeles date +%F)"

cd "$ROOT"

if [ ! -s recipients.csv ]; then
  echo "SKIP $(TZ=America/Los_Angeles date '+%F %T %Z') recipients.csv missing or empty" >> "$LOG"
  exit 0
fi

if [ ! -f "daily_papers/$today.md" ]; then
  echo "SKIP $(TZ=America/Los_Angeles date '+%F %T %Z') daily_papers/$today.md missing" >> "$LOG"
  exit 0
fi

python3 scripts/verify_publish.py --date "$today" >> "$LOG" 2>&1
python3 paper_daily_email.py --date "$today" >> "$LOG" 2>&1
