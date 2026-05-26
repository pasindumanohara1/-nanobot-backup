"""
One-shot CSE heartbeat runner.
Fetches trade data, parses changed stocks, and outputs for OWL to send via message tool.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reset the price tracker so all changed stocks show up
import cse_scraper
cse_scraper.last_sent_prices = {}

from cse_scraper import fetch_trade_summary, parse_movements, format_message, chunk_movements

data = fetch_trade_summary()
if not data:
    print("ERROR: No data")
    sys.exit(1)

movements = parse_movements(data)
print(f"Changed stocks found: {len(movements)}")

if movements:
    chunks = chunk_movements(movements)
    total = len(chunks)
    print(f"Chunks: {total}")
    for i, chunk in enumerate(chunks):
        msg = format_message(chunk, part_num=i+1, total_parts=total)
        print(f"\n--- Chunk {i+1}/{total} ({len(msg)} chars, {len(chunk)} stocks) ---")
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode("ascii", errors="replace").decode())
    print(f"\nDone! {total} message(s) ready.")
else:
    print("No changed stocks.")
