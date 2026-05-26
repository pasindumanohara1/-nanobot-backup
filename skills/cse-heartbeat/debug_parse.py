import sys, json
sys.path.insert(0, '.')
from cse_scraper import fetch_trade_summary, parse_movements

data = fetch_trade_summary()
if not data:
    print("ERROR: fetch_trade_summary returned None")
    sys.exit(1)

stocks = data.get('reqTradeSummery', [])
print(f"Total stocks in response: {len(stocks)}")

# Manually check how many pass the threshold
threshold = 2.0
count = 0
for stock in stocks:
    try:
        pct = float(str(stock.get('percentageChange', 0)).replace('+', '').replace('%', '').strip())
        if abs(pct) >= threshold:
            count += 1
            if count <= 5:
                ticker = stock.get('symbol', '').split('.')[0]
                print(f"  {ticker}: {pct}% (price={stock.get('price')}, change={stock.get('change')})")
    except:
        pass

print(f"\nStocks >= {threshold}%: {count}")

# Now test parse_movements
movements = parse_movements(data)
print(f"parse_movements returned: {len(movements)} items")
for m in movements[:5]:
    print(f"  {m['ticker']}: {m['change_pct']}%")
