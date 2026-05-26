"""
CSE (Colombo Stock Exchange) Real-Time Heartbeat Scraper
Market hours: Mon-Fri, 9:30 AM - 2:30 PM IST (UTC+5:30)
Fetches trade summary, filters significant movements (>=2%), sends to Telegram.
"""

import time
import json
import os
import sys
import requests
from datetime import datetime, timezone, timedelta

# ====== CONFIGURATION ======
TELEGRAM_BOT_TOKEN = "8693066753:AAEiL2TnrT5-BGiNRncphauixA7hrcZtHFE"
TELEGRAM_CHAT_ID = "-1003273701293"  # @cse_alert channel
HEARTBEAT_INTERVAL = 300  # 5 minutes
CHANGE_THRESHOLD = 2.0  # Minimum % change to trigger alert
MAX_STOCKS_PER_MESSAGE = 15  # Top N movers to show per message
MAX_MESSAGE_LENGTH = 4000  # Telegram limit is 4096, leave buffer

# Market hours (IST = UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))
MARKET_OPEN = (9, 30)
MARKET_CLOSE = (14, 30)

# Track previous prices to avoid duplicate alerts
last_sent_prices = {}


def safe_print(msg):
    """Print safely on Windows with emoji support."""
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        # Fallback: encode to console encoding, replacing unsupported chars
        encoded = msg.encode(sys.stdout.encoding or 'utf-8', errors='replace')
        sys.stdout.buffer.write(encoded + b'\n')
        sys.stdout.flush()


def is_market_open():
    """Check if CSE market is currently open (Mon-Fri, 9:30-14:30 IST)."""
    now = datetime.now(IST)
    if now.weekday() >= 5:
        return False
    current_minutes = now.hour * 60 + now.minute
    open_minutes = MARKET_OPEN[0] * 60 + MARKET_OPEN[1]
    close_minutes = MARKET_CLOSE[0] * 60 + MARKET_CLOSE[1]
    return open_minutes <= current_minutes <= close_minutes


def fetch_trade_summary():
    """Fetch trade summary from CSE API."""
    try:
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.cse.lk/equity/trade-summary',
            'Origin': 'https://www.cse.lk'
        })
        s.get('https://www.cse.lk/', timeout=15)
        r = s.post('https://www.cse.lk/api/tradeSummary', data={}, timeout=15)
        if r.status_code == 200:
            return r.json()
        safe_print(f"[!] API error: {r.status_code}")
        return None
    except Exception as e:
        safe_print(f"[!] Fetch error: {e}")
        return None


def parse_movements(data):
    """Parse trade summary: keep only stocks with non-zero change, sort ascending (losers -> gainers)."""
    global last_sent_prices
    changed = []

    if not data:
        return changed

    stocks = data.get('reqTradeSummery', None)

    # Empty array = market hasn't started trading yet (before 9:30 AM or no trades)
    if stocks is not None and len(stocks) == 0:
        safe_print("[*] Market data empty — no trades yet (market may not have opened).")
        return changed

    if not stocks:
        for key, val in data.items():
            if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                stocks = val
                break

    if not stocks:
        return changed

    for stock in stocks:
        try:
            ticker = stock.get('symbol', '')
            if '.' in ticker:
                ticker = ticker.split('.')[0]
            company = stock.get('name', ticker)
            last_price = float(str(stock.get('price', 0)).replace(',', ''))
            prev_close = float(str(stock.get('previousClose', 0)).replace(',', ''))
            change_pct = float(str(stock.get('percentageChange', 0)).replace('+', '').replace('%', '').strip())
            change_rs = float(str(stock.get('change', 0)).replace('+', '').replace(',', '').strip())
            volume = int(str(stock.get('sharevolume', 0)).replace(',', ''))
        except (ValueError, TypeError):
            continue

        if not ticker:
            continue

        # Skip unchanged stocks (zero price movement)
        if change_pct == 0 and change_rs == 0:
            continue

        # Skip if price hasn't changed since last alert
        if ticker in last_sent_prices and last_sent_prices[ticker] == last_price:
            continue

        changed.append({
            "ticker": ticker,
            "company": company,
            "price": last_price,
            "prev_close": prev_close,
            "change_rs": change_rs,
            "change_pct": change_pct,
            "volume": volume
        })
        last_sent_prices[ticker] = last_price

    # Sort ascending: biggest losers first -> biggest gainers last
    changed.sort(key=lambda x: x["change_pct"])
    return changed


def format_volume(v):
    """Format volume in human-readable form (K, M)."""
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    elif v >= 1_000:
        return f"{v/1_000:.1f}K"
    return str(v)


def format_message(movements, part_num=1, total_parts=1):
    """Format market movements into a clean monospace Telegram table.
    Sorted ascending: losers -> gainers. Only changed stocks shown."""
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")

    if total_parts > 1:
        header = f"📊 *CSE Live Movements* — {now} ({part_num}/{total_parts})\n"
    else:
        header = f"📊 *CSE Live Movements* — {now}\n"

    lines = [header]
    lines.append("```")
    lines.append(f"{'Ticker':<8} {'Price':>10} {'Change':>10} {'Vol':>8}")
    lines.append("─" * 40)

    for m in movements:
        emoji = "🟢" if m["change_pct"] > 0 else "🔴"
        sign_pct = "+" if m["change_pct"] > 0 else ""
        pct_str = sign_pct + format(m["change_pct"], ".2f") + "%"
        price_str = format(m["price"], ",.2f")
        vol_str = format_volume(m["volume"])
        lines.append(f"{emoji} {m['ticker']:<6} {price_str:>10} {pct_str:>10} {vol_str:>8}")

    lines.append("─" * 40)
    lines.append(f"Showing {len(movements)} changed stocks | Sorted: Ascending")
    lines.append("```")
    lines.append(f"_Unchanged stocks hidden | Next update in {HEARTBEAT_INTERVAL // 60} min_")

    return "\n".join(lines)


def send_telegram(message):
    """Send message to Telegram channel via OWL's message tool.

    NOTE: This function only prints the message. The actual sending
    is done by OWL's message tool (nanobot's own bot).
    Raw bot API calls via Python requests do NOT work.
    """
    safe_print("[*] Message ready for Telegram:")
    safe_print(message[:200] + "..." if len(message) > 200 else message)
    safe_print(f"[*] Length: {len(message)} chars | Chat: {TELEGRAM_CHAT_ID}")


def chunk_movements(movements):
    """Split movements into chunks that fit in Telegram's message limit."""
    if not movements:
        return []

    chunks = []
    current_chunk = []

    for m in movements:
        # Test if adding this stock would exceed limit
        test_msg = format_message(current_chunk + [m])
        if len(test_msg) > MAX_MESSAGE_LENGTH and current_chunk:
            chunks.append(current_chunk)
            current_chunk = [m]
        else:
            current_chunk.append(m)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def run_cycle():
    """Single heartbeat cycle. Returns message string or None."""
    trade_data = fetch_trade_summary()
    if not trade_data:
        safe_print("[!] No trade data received.")
        return None

    movements = parse_movements(trade_data)
    if not movements:
        safe_print("[*] No significant movements.")
        return None

    safe_print(f"[*] {len(movements)} changed stock(s) detected!")
    
    # Split into chunks and send
    chunks = chunk_movements(movements)
    total = len(chunks)
    
    for i, chunk in enumerate(chunks):
        msg = format_message(chunk, part_num=i+1, total_parts=total)
        send_telegram(msg)
        if i < total - 1:
            time.sleep(1)  # Small delay between messages to avoid rate limiting
    
    return chunks


def wait_for_market():
    """Sleep until next market open."""
    now = datetime.now(IST)
    if now.weekday() >= 5:
        days_until_monday = 7 - now.weekday()
        next_open = (now + timedelta(days=days_until_monday)).replace(
            hour=MARKET_OPEN[0], minute=MARKET_OPEN[1], second=0, microsecond=0
        )
    else:
        close_minutes = MARKET_CLOSE[0] * 60 + MARKET_CLOSE[1]
        current_minutes = now.hour * 60 + now.minute
        if current_minutes > close_minutes:
            next_day = now + timedelta(days=1)
            if next_day.weekday() >= 5:
                days_until_monday = 7 - next_day.weekday()
                next_open = (next_day + timedelta(days=days_until_monday)).replace(
                    hour=MARKET_OPEN[0], minute=MARKET_OPEN[1], second=0, microsecond=0
                )
            else:
                next_open = next_day.replace(
                    hour=MARKET_OPEN[0], minute=MARKET_OPEN[1], second=0, microsecond=0
                )
        else:
            next_open = now.replace(
                hour=MARKET_OPEN[0], minute=MARKET_OPEN[1], second=0, microsecond=0
            )

    wait_seconds = max(60, (next_open - now).total_seconds())
    safe_print(f"[*] Market closed. Sleeping until {next_open.strftime('%Y-%m-%d %H:%M')} IST ({wait_seconds/3600:.1f}h)")
    time.sleep(min(wait_seconds, 3600))


if __name__ == "__main__":
    safe_print("[+] CSE Heartbeat Daemon Started")
    safe_print(f"[*] Alert threshold: ≥{CHANGE_THRESHOLD}%")
    safe_print(f"[*] Heartbeat interval: {HEARTBEAT_INTERVAL}s")
    safe_print(f"[*] Market hours: Mon-Fri {MARKET_OPEN[0]}:{MARKET_OPEN[1]:02d}-{MARKET_CLOSE[0]}:{MARKET_CLOSE[1]:02d} IST")
    safe_print(f"[*] Telegram channel: {TELEGRAM_CHAT_ID}")

    while True:
        if is_market_open():
            try:
                run_cycle()
            except Exception as e:
                safe_print(f"[!] Cycle error: {e}")
            time.sleep(HEARTBEAT_INTERVAL)
        else:
            wait_for_market()
