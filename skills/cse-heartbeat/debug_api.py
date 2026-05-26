import requests, json, sys, os

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_log.txt")

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

log("=== CSE API Debug ===")
log(f"requests version: {requests.__version__}")

try:
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.cse.lk/equity/trade-summary',
        'Origin': 'https://www.cse.lk'
    })
    
    log("Step 1: GET main page...")
    r0 = s.get('https://www.cse.lk/', timeout=15)
    log(f"  Status: {r0.status_code}, Length: {len(r0.text)}")
    
    log("Step 2: POST tradeSummary...")
    r = s.post('https://www.cse.lk/api/tradeSummary', data={}, timeout=15)
    log(f"  Status: {r.status_code}, Length: {len(r.text)}")
    log(f"  Response (first 1000):\n{r.text[:1000]}")
    
    if r.status_code == 200:
        try:
            data = r.json()
            log(f"  JSON keys: {list(data.keys())}")
            
            stocks = data.get('reqTradeSummery', None)
            if stocks is None:
                # Search for any list of dicts
                for key, val in data.items():
                    if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                        stocks = val
                        log(f"  Found stocks under key: '{key}' ({len(val)} items)")
                        break
            
            if stocks:
                log(f"  Total stocks: {len(stocks)}")
                log(f"  First stock keys: {list(stocks[0].keys())}")
                log(f"  First stock sample:\n{json.dumps(stocks[0], indent=2)}")
                
                # Check field names the scraper expects
                sample = stocks[0]
                log(f"\n  Field check:")
                log(f"    'symbol' present: {'symbol' in sample}, value: {sample.get('symbol', 'N/A')}")
                log(f"    'name' present: {'name' in sample}, value: {sample.get('name', 'N/A')}")
                log(f"    'price' present: {'price' in sample}, value: {sample.get('price', 'N/A')}")
                log(f"    'previousClose' present: {'previousClose' in sample}, value: {sample.get('previousClose', 'N/A')}")
                log(f"    'percentageChange' present: {'percentageChange' in sample}, value: {sample.get('percentageChange', 'N/A')}")
                log(f"    'change' present: {'change' in sample}, value: {sample.get('change', 'N/A')}")
                log(f"    'sharevolume' present: {'sharevolume' in sample}, value: {sample.get('sharevolume', 'N/A')}")
                log(f"    'lastTradedPrice' present: {'lastTradedPrice' in sample}, value: {sample.get('lastTradedPrice', 'N/A')}")
                log(f"    'changePercentage' present: {'changePercentage' in sample}, value: {sample.get('changePercentage', 'N/A')}")
                log(f"    'volume' present: {'volume' in sample}, value: {sample.get('volume', 'N/A')}")
            else:
                log("  ERROR: No stock list found in response!")
        except Exception as e:
            log(f"  JSON parse error: {e}")
    else:
        log(f"  Non-200 response: {r.text[:500]}")
        
except Exception as e:
    log(f"Exception: {e}")

log("=== Done ===")
