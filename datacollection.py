import requests

cursor = ''
election_list = []

for i in range(1,100):
    
    if cursor == '':
        url = "https://api.elections.kalshi.com/trade-api/v2/events?status=closed,settled&limit=200"
    else:
        url = "https://api.elections.kalshi.com/trade-api/v2/events?status=closed,settled&limit=200&cursor=" + cursor
    
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_dic = response.json()
    cursor = response_dic['cursor']
    event_dic = response_dic['events']

    for event in event_dic:
        if 'Who will win the Presidential Election?' in event['title']:
            election_list.append(event)
    
event_ticker = election_list[0]['event_ticker']

url = 'https://api.elections.kalshi.com/trade-api/v2/markets?event_ticker=' + event_ticker
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
response_dic = response.json()

dt_market = response_dic['markets'][2]
dt_ticker = dt_market['ticker']

trades = []
cursor = ''
url = 'https://api.elections.kalshi.com/trade-api/v2/markets/trades'

while True:
    
    params = {
        "ticker": dt_ticker,
        "limit": 1000,
        "cursor": cursor
    }
    
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    response_dic = response.json()
    cursor = response_dic['cursor']
    
    trades += response_dic['trades']
    if len(response_dic['trades']) < 1000:
        break
    

    
