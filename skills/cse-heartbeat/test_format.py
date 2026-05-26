import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cse_scraper
cse_scraper.last_sent_prices = {}

from cse_scraper import fetch_trade_summary, parse_movements, format_message, chunk_movements, send_telegram

print("Fetching data...", flush=True)
data = fetch_trade_summary()
if not data:
    print("ERROR: No data")
    sys.exit(1)

movements = parse_movements(data)
print(f"Changed stocks: {len(movements)}", flush=True)

if movements:
    chunks = chunk_movements(movements)
    total = len(chunks)
    print(f"Chunks: {total}", flush=True)

    # Write first chunk to file for preview
    with open("preview_output.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            msg = format_message(chunk, part_num=i+1, total_parts=total)
            f.write(f"\n--- Chunk {i+1}/{total} ({len(msg)} chars, {len(chunk)} stocks) ---\n")
            f.write(msg + "\n")

    # Send all chunks to Telegram
    for i, chunk in enumerate(chunks):
        msg = format_message(chunk, part_num=i+1, total_parts=total)
        print(f"Sending chunk {i+1}/{total} ({len(msg)} chars)...", flush=True)
        send_telegram(msg)
        if i < total - 1:
            import time
            time.sleep(1)

    print("Done!", flush=True)
else:
    print("No changed stocks.", flush=True)
