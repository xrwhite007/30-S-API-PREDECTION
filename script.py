import requests
import json
import time

HISTORY_API = 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'

def fetch_and_update():
    try:
        # API থেকে ডাটা আনা
        response = requests.get(HISTORY_API, timeout=10)
        data = response.json()
        history_list = data['data']['list']
        
        # পিরিয়ড এবং ম্যাথ লজিক
        last_period = int(history_list[0]['issueNumber'])
        next_period = last_period + 1
        n1 = int(history_list[0]['number'])
        
        # আপনার দেওয়া ম্যাথ লজিক
        pred1 = "Small" if n1 >= 5 else "Big"  # বিপরীত লজিক
        pred2 = "Big" if n1 % 2 == 0 else "Small" # জোড়-বিজোড় লজিক

        # JSON ফরম্যাটে ডাটা সাজানো
        output = {
            "next_period": next_period,
            "prediction_1": pred1,
            "prediction_2": pred2,
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        with open('data.json', 'w') as f:
            json.dump(output, f, indent=4)
            
        print(f"JSON Updated: Period {next_period} | Pred: {pred1}")
    except Exception as e:
        print(f"Error fetching data: {e}")

# এক মিনিটের সাইকেলে ২ বার রান হবে (প্রতি ৩০ সেকেন্ডে)
for i in range(2):
    fetch_and_update()
    if i == 0:
        time.sleep(27) # পরের ড্র এর আগে আপডেট করার জন্য ২৭ সেকেন্ড গ্যাপ
