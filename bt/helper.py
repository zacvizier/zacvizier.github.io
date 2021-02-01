import requests

import datetime
import csv

START_TIME = 6
START_MINUTE = 30

END_TIME = 13
END_MINUTE = 0
STOCK_TICKER = "COST"
FILE_NAME = "test1.csv"

def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

def main():
    from_ = "2021-01-06"
    to_ = "2021-01-15"

    url = "https://api.polygon.io/v2/aggs/ticker/" + STOCK_TICKER + "/range/1/minute/" + from_ + "/" + to_ + "?limit=50000&sort=asc&apiKey=0MUvBkBmcpUWIp1lZDpTK3AxIqhOnsaW"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.json()['results'])

    fullFileName = STOCK_TICKER + FILE_NAME
    with open(fullFileName, mode='w') as csv_file:
            fieldnames = ['time', 'open', 'high', 'low', 'close', 'volume']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'time': 'time', 'open': 'open', 
                    'high': 'high', 'low': 'low', 
                    'close': 'close', 'volume': 'volume'})
            for result in response.json()['results']: #response.json():
                #print(result)
                dt = ts_to_datetime(result["t"])
                dt_hour = dt.split(":")[0][-2:]
                dt_minute = dt.split(":")[1][:2]
                if((int(dt_hour) < END_TIME) and ((int(dt_hour) > START_TIME) or ((int(dt_hour) == START_TIME) and (int(dt_minute) >= START_MINUTE)))):
                    writer.writerow({'time': dt, 'open': result['o'], 
                        'high': result['h'], 'low': result['l'], 
                        'close': result['c'], 'volume': result['v']})

    #print(response.results)
    #print(response.json()['results'])


if __name__ == '__main__':
    main()