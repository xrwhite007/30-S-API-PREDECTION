import requests
import json
import time

# 30S API Endpoint
HISTORY_API = 'https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json'

def get_math_logic(history):
    # Box 1 Logic: Opposite of last result
    n1 = int(history[0]['number'])
    n2 = int(history[1]['number'])
    
    pred1 = "Small" if n1 >= 5 else "Big"
    
    # Box 2 Logic: Sum of last two
    pred2 = "Big" if (n1 + n2) % 2 == 0 else "Small"
    
    # Smart Signal: Randomly choosing one as main or based on your logic
    # এখানে আমরা Box 1 কে Primary ধরছি
    return pred1, pred2

def main():
    try:
        response = requests.get(HISTORY_API)
        data = response.json()
        history_list = data['data']['list']
        
        # Next Period calculation
        last_period = int(history_list[0]['issueNumber'])
        next_period = last_period + 1
        
        pred1, pred2 = get_math_logic(history_list)
        
        # JSON Output
        output_data = {
            "next_period": next_period,
            "prediction_1": pred1,
            "prediction_2": pred2,
            "main_signal": pred1, # আপনি চাইলে এটি পরিবর্তন করতে পারেন
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open('data.json', 'w') as f:
            json.dump(output_data, f, indent=4)
        print(f"Successfully updated Period: {next_period}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
