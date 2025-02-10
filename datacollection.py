import requests
import pandas as pd
from time import sleep

def get_events(query_str = '', status = ''): # Query for Kalshi events. Will only include events with query_str.

    # status param is to filter for events with certain status (closed, settled, unopened, open). 
    # Seperate statuses with commas.
    
    cursor = ''
    event_list = []

    url = "https://api.elections.kalshi.com/trade-api/v2/events"

    while True:
        
        if status == '':
            params = {
                'cursor': cursor,
                'limit': 200
                }
            
        else:
            params = {
                'cursor': cursor,
                'limit': 200,
                'status': status
                }

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers, params = params)
        response_dic = response.json()
        cursor = response_dic['cursor']
        event_dic = response_dic['events']

        for event in event_dic:
            if query_str in event['title']:
                event_list.append(event)
        
        if len(event_dic) < 200:
            break
        
    return event_list

def get_markets(event_ticker, query_str = ''): # Returns list of markets for event with ticker event_id (str)
    
    # can query for specific markets with query_str

    url = 'https://api.elections.kalshi.com/trade-api/v2/markets?event_ticker=' + event_ticker
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_dic = response.json()
    
    markets = response_dic['markets']
    
    if query_str != '':
        
        markets_q = []
        for market in markets:
            if query_str in market['title']:
                markets_q.append(market)
        
        return markets_q
    
    return markets

def get_trades(market_ticker): # returns list of trades made with market (with id market_ticker)
    
    trades = []
    cursor = ''
    url = 'https://api.elections.kalshi.com/trade-api/v2/markets/trades'

    while True:
        
        params = {
            "ticker": market_ticker,
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
        
        sleep(1)
    
    return trades

pres_events = get_events('Presidential Election', status = 'closed,settled')
djt_market = get_markets(pres_events[0]['event_ticker'], query_str='Trump')
djt_trades = get_trades(djt_market[0]['ticker'])





    
