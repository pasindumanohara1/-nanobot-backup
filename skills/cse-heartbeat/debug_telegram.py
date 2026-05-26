import requests, json

BOT_TOKEN = "8693066753:AAEiL2TnrT5-BGiNRncphauixA7hrcZtHFE"
CHAT_ID = "-1003273701293"

# Test 1: Simple text message
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "🧪 CSE Bot test message - simple text",
    "disable_web_page_preview": True,
}
print("Sending simple text...", flush=True)
r = requests.post(url, json=payload, timeout=15)
print(f"Status: {r.status_code}", flush=True)
print(f"Response: {r.text[:500]}", flush=True)

# Test 2: Markdown message
payload2 = {
    "chat_id": CHAT_ID,
    "text": "🧪 *CSE Bot test* — _Markdown_ message",
    "parse_mode": "Markdown",
    "disable_web_page_preview": True,
}
print("\nSending markdown text...", flush=True)
r2 = requests.post(url, json=payload2, timeout=15)
print(f"Status: {r2.status_code}", flush=True)
print(f"Response: {r2.text[:500]}", flush=True)

# Test 3: getChat to verify bot is in channel
url3 = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
print("\nChecking bot access to channel...", flush=True)
r3 = requests.post(url3, json={"chat_id": CHAT_ID}, timeout=15)
print(f"Status: {r3.status_code}", flush=True)
print(f"Response: {r3.text[:500]}", flush=True)

# Test 4: getMe
url4 = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
print("\nChecking bot info...", flush=True)
r4 = requests.get(url4, timeout=15)
print(f"Status: {r4.status_code}", flush=True)
print(f"Response: {r4.text[:500]}", flush=True)
