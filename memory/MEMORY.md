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
- Scrapes Colombo Stock Exchange trade summary API, sends alerts to Telegram channel @cse_alert (chat ID: -1003273701293) when stock movements ≥2%
- Script: `C:\Users\pasindu\Desktop\automation\cse-heartbeat\cse_scraper.py`
- API endpoint: `https://www.cse.lk/api/tradeSummary` (POST with form data, not JSON); response key: `reqTradeSummery`; fields: `symbol`, `name`, `lastTradedPrice`, `changePercentage`, `change`, `volume`
- Heartbeat interval: 300 seconds (5 minutes); filtering threshold: ≥2% price change
- Trading hours: Monday–Friday, 9:30am–2:30pm
- Nanobot agent URL: `http://localhost:8000/nanobot/agent/run`
- All Telegram posting goes through OWL's message tool (nanobot's own bot); raw bot API calls via Python requests do NOT work
- Bot token `8693066753:AAEiL2TnrT5-BGiNRncphauixA7hrcZtHFE` was provided but is NOT used — nanobot's own bot handles all Telegram posting
- Skill created at `skills/cse-heartbeat/` with SKILL.md and cse_scraper.py
- Old deleted files from cse-heartbeat folder: `run.py`, `test_api.py`, `telegram_post.py`, `output.json`
- Cron job `daily-trending-post` exists (id: af7bbc63, cron: `0 9 * * * UTC`) — purpose unclear, may need updating for CSE heartbeat schedule
- Scraper output was empty at last check — parsing issue with API response fields still needs debugging

### Vidbanda Movie Poster
- Posts movie info + banner to Telegram channel (chat ID: -1003809102397) using `generate_post.py` + OWL message tool

### Other
- MarketWatch Sri Lanka page is an alternative CSE data source but blocks repeated requests (rate limiting)
- Reference GitHub repo for MarketWatch approach: https://github.com/bhagyawarnakulasooriya/cse_marketdata_dashboard

---

*This file is automatically updated by nanobot when important information should be remembered.*
