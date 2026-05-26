# Heartbeat Tasks

This file is checked every 30 minutes by your nanobot agent.
Add tasks below that you want the agent to work on periodically.

If this file has no tasks (only headers and comments), the agent will skip the heartbeat.

## Active Tasks

### CSE Market Heartbeat
- **What**: Run the CSE scraper to fetch live trade data and post changed stocks to Telegram
- **When**: Every 5 minutes during market hours (Mon-Fri, 9:30 AM - 2:30 PM IST / 4:00 UTC - 9:00 UTC)
- **How**: 
  1. Check current UTC time — only proceed if Mon-Fri, 4:00-9:00 UTC
  2. Execute `cd C:\Users\pasindu\.nanobot\workspace\skills\cse-heartbeat && python run_once.py`
  3. Read the output — each chunk is prefixed with `--- Chunk N/M ---`
  4. For each chunk, send it via the `message` tool to chat ID `-1003273701293` (channel @cse_alert)
  5. Add a small delay between sending chunks to avoid Telegram rate limiting
- **Note**: Only post if there are changed stocks. Skip weekends and outside market hours.
- **Output**: Monospace table, sorted ascending (losers → gainers), 🟢/🔴 indicators, auto-split if >4096 chars
- **Send method**: OWL message tool → @cse_alert (chat ID: -1003273701293)
- **Important**: Do NOT create a cron job for this. The heartbeat interval handles it.


## Completed

<!-- Move completed tasks here or delete them -->
