import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cse_scraper
cse_scraper.last_sent_prices = {}
from cse_scraper import fetch_trade_summary, parse_movements, format_message, chunk_movements

data = fetch_trade_summary()
if not data:
    print('NO DATA')
    sys.exit(1)

movements = parse_movements(data)
chunks = chunk_movements(movements)

for i in [1, 2]:
    msg = format_message(chunks[i], part_num=i+1, total_parts=3)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'chunk{i+1}.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(msg)
    print(f'Wrote chunk {i+1} ({len(msg)} chars)')
