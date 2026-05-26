# CSE Heartbeat

Colombo Stock Exchange market data scraper that posts significant stock movements to a Telegram channel.

## Trigger

Use this skill when the user wants to:
- Fetch CSE market data / trade summary
- Post stock market alerts to @cse_alert Telegram channel
- Check which stocks changed (any non-zero movement)
- Start/stop the CSE heartbeat daemon

## How It Works

1. Fetches live trade summary from `https://www.cse.lk/api/tradeSummary`
2. Parses all ~290 stocks, filters out unchanged (zero movement) stocks
3. Sorts ascending: biggest losers first → biggest gainers last
4. Formats a clean monospace table with 🟢/🔴 indicators
5. Splits into multiple messages if needed (Telegram 4096 char limit)
6. Sends to @cse_alert channel (`-1003273701293`) via OWL's message tool

**Important:** All Telegram posting goes through OWL's message tool. Raw bot API calls via Python `requests` do NOT work. The bot token in the script is unused.

## Quick Commands

### Fetch and post now (one-shot)
```bash
cd C:\Users\pasindu\.nanobot\workspace\skills\cse-heartbeat
python run_once.py
```

This prints the formatted message(s). OWL then sends them via the `message` tool to the Telegram channel.

### Start the heartbeat daemon (runs continuously)
```bash
python C:\Users\pasindu\.nanobot\workspace\skills\cse-heartbeat\cse_scraper.py
```

The daemon:
- Runs only during market hours (Mon-Fri, 9:30 AM - 2:30 PM IST)
- Checks every 5 minutes
- Shows ALL changed stocks (non-zero movement), sorted ascending (losers → gainers)
- Avoids duplicate alerts (tracks last sent prices)
- Sleeps automatically when market is closed
- Uses monospace table format with 🟢/🔴 indicators
- Auto-splits into multiple messages if >4096 chars

**Note:** The daemon's `send_telegram()` only prints messages. OWL sends them via the `message` tool.

## Configuration

Edit `cse_scraper.py` to change:
- `CHANGE_THRESHOLD` — minimum % change to trigger alert (default: 2.0)
- `HEARTBEAT_INTERVAL` — seconds between checks (default: 300)
- `TELEGRAM_CHAT_ID` — target channel (default: -1003273701293)
- `TELEGRAM_BOT_TOKEN` — bot token (default: 8693066753:...)

## API Details

- **Endpoint**: `POST https://www.cse.lk/api/tradeSummary`
- **Auth**: None required (public API)
- **Headers needed**: `Referer: https://www.cse.lk/`, `Origin: https://www.cse.lk`
- **Response key**: `reqTradeSummery` (array of ~293 stocks)
- **Stock fields**: `symbol`, `name`, `lastTradedPrice`, `changePercentage`, `change`, `volume`

## Telegram

- **Channel**: @cse_alert (`-1003273701293`)
- **Posting method**: OWL's message tool (nanobot's own bot) — NOT raw API calls
- **Note**: Bot token `8693066753:AAEiL2TnrT5-BGiNRncphauixA7hrcZtHFE` exists in script but is NOT used

## Files

- `cse_scraper.py` — Main scraper + daemon script
- `run_one.py` — One-shot runner (resets `last_sent_prices` each run for testing)
- `SKILL.md` — This file
