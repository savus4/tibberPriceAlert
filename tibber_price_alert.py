import os
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from pushover_complete import PushoverAPI
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TIBBER_TOKEN = os.getenv('TIBBER_TOKEN')
PUSHOVER_TOKEN = os.getenv('PUSHOVER_TOKEN')
PUSHOVER_GROUP = os.getenv('PUSHOVER_GROUP')

TIBBER_API_URL = 'https://api.tibber.com/v1-beta/gql'

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_prices():
    headers = {
        'Authorization': f'Bearer {TIBBER_TOKEN}',
        'Content-Type': 'application/json',
    }
    query = '''
    { 
      viewer {
        homes {
          currentSubscription {
            priceInfo {
              today { total startsAt }
              tomorrow { total startsAt }
            }
          }
        }
      }
    }
    '''
    response = requests.post(TIBBER_API_URL, json={'query': query}, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def find_negative_prices(data):
    homes = data['data']['viewer']['homes']
    if not homes:
        return []
    price_info = homes[0]['currentSubscription']['priceInfo']
    prices = (price_info.get('tomorrow') or [])
    negative_prices = [p for p in prices if p['total'] < 0]
    return negative_prices

def send_push_notification(prices):
    po = PushoverAPI(PUSHOVER_TOKEN)
    message = 'Negativer Strompreis morgen!\n'
    for p in prices:
        time = datetime.fromisoformat(p['startsAt']).strftime('%Y-%m-%d %H:%M')
        message += f"{time}: {p['total']} €/kWh\n"
    message = message.strip()
    po.send_message(PUSHOVER_GROUP, message, title='Tibber Negativ-Preis Alarm', priority=1)

def main():
    try:
        data = fetch_prices()
        negative_prices = find_negative_prices(data)
        if negative_prices:
            send_push_notification(negative_prices)
        else:
            print('No negative prices found.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
