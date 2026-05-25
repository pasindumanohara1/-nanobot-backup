# Long-term Memory

This file stores important information that should persist across sessions.

## User Information

- Full name: Pasindu Manohara
- Username: @Pasindumanohara
- Telegram ID: 1721575073
- Location: Sri Lanka
- OS: Windows
- Working directory: `C:\Users\pasindu\Desktop\automation\`
- Python version: 3.12

## Preferences

- Uses TMDB and IMDB for movie/TV data
- Prefers automation workflows for social media posting
- WhatsApp Newsletter channel for posting content

## Project Context

### CSE Heartbeat
- Scrapes Colombo Stock Exchange trade summary API, posts ALL changed stocks to Telegram channel @cse_alert (chat ID: -1003273701293)
- Script: `C:\Users\pasindu\.nanobot\workspace\skills\cse-heartbeat\cse_scraper.py`
- Runner: `C:\Users\pasindu\.nanobot\workspace\skills\cse-heartbeat\run_once.py`
- API endpoint: `https://www.cse.lk/api/tradeSummary` (POST with form data); response key: `reqTradeSummery`; fields: `symbol`, `name`, `lastTradedPrice`, `changePercentage`, `change`, `volume`
- Shows ALL changed stocks (non-zero movement), sorted ascending (losers → gainers)
- Format: monospace table with 🟢/🔴 indicators, auto-splits into multiple messages if >4096 chars
- ~220 out of 290 stocks typically show non-zero movement
- Heartbeat interval: 300 seconds (5 minutes)
- Trading hours: Monday–Friday, 9:30am–2:30pm IST (4:00-9:00 UTC)
- Cron job `cse-heartbeat-5min` (id: 9c14f3c3) — **PAUSED** at user's request (~10:44 UTC 2026-05-25); user confirmed keeping it paused
- Root cause of intermittent delivery: cron previously ran 24/7 outside market hours causing Telegram rate-limiting; schedule was restricted to `*/5 4-9 * * 1-5 UTC` before pause
- All Telegram posting goes through OWL's message tool (nanobot's own bot); raw bot API calls via Python requests do NOT work
- `send_telegram()` in cse_scraper.py only prints — OWL sends via message tool
- `run_once.py` resets `last_sent_prices` each run for testing

### Vidbanda Movie Poster
- Posts movie/TV info + banner to Telegram channel (chat ID: -1003809102397)
- Script: `C:\Users\pasindu\Desktop\automation\fb_post_maker\scripts\generate_post.py`
- **Fix applied (2026-05-25):** Numeric TMDB IDs now tried directly first instead of being prefixed with `tt`
- Banner folder: `C:\Users\pasindu\Desktop\automation\fb_post_maker\fb_banners\`
- Output file: `C:\Users\pasindu\Desktop\automation\fb_post_maker\output.json`
- Watch link format: `https://www.vidbanda.duckdns.org/details/<type>/<tmdb_id>`
- Banner naming: `<tmdb_id>_<type>.jpg`

### Islamic Post Generator
- Skill created at `C:\Users\pasindu\.nanobot\workspace\skills\islamic-post-generator/`
- Supports 5 post types: quran, hadith, dhikr, dua, reminder
- User wants Islamic posts sent to their Telegram (ID: 1721575073); unclear if a dedicated channel is needed

### Other
- MarketWatch Sri Lanka page is an alternative CSE data source but blocks repeated requests (rate limiting)
- Reference GitHub repo for MarketWatch approach: https://github.com/bhagyawarnakulasooriya/cse_marketdata_dashboard
- File `prayer-times-apis.txt` created at `C:\Users\pasindu\Desktop\automation\prayer-times-apis.txt`
- Movie/TV Telegram channel chat_id: -1003809102397

---

*This file is automatically updated by nanobot when important information should be remembered.*
