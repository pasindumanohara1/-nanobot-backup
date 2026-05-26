import sys
sys.path.insert(0, '.')
from cse_scraper import fetch_trade_summary, parse_movements, format_message, send_telegram

print("=== Full Cycle Test ===", flush=True)

data = fetch_trade_summary()
if not data:
    print("ERROR: No data", flush=True)
    sys.exit(1)

movements = parse_movements(data)
print(f"Movements: {len(movements)}", flush=True)

if movements:
    msg = format_message(movements)
    print(f"Message length: {len(msg)}", flush=True)
    print("--- MESSAGE PREVIEW ---", flush=True)
    print(msg[:800], flush=True)
    print("--- SENDING TO TELEGRAM ---", flush=True)
    send_telegram(msg)
else:
    print("No significant movements.", flush=True)
