"""One-shot CSE scraper runner. Fetches data, prints formatted chunks, resets last_sent_prices."""
import sys, os, io
sys.path.insert(0, os.path.dirname(__file__))

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import cse_scraper

# Reset last_sent_prices for fresh run
cse_scraper.last_sent_prices = {}

trade_data = cse_scraper.fetch_trade_summary()
if not trade_data:
    print("ERROR: No trade data received.")
    sys.exit(1)

movements = cse_scraper.parse_movements(trade_data)
if not movements:
    print("No significant movements.")
    sys.exit(0)

chunks = cse_scraper.chunk_movements(movements)

# Write each chunk to a separate file for easy reading
for i, chunk in enumerate(chunks):
    msg = cse_scraper.format_message(chunk, part_num=i+1, total_parts=len(chunks))
    filepath = os.path.join(os.path.dirname(__file__), f'chunk{i+1}.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(msg)
    print(f"Chunk {i+1}/{len(chunks)}: {len(chunk)} stocks, {len(msg)} chars -> {filepath}")

print(f"Done! {len(chunks)} chunks written.")
