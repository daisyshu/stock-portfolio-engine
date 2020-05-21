import requests
import json

def fetchStockStatistics(symbol):
        """
        Fetches stock statistics, and returns GET response for stock interested.
        """
        urlStats = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
        queryStringStats = {"region": "US","symbol": symbol}
        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
            }
        response = requests.request("GET", urlStats, headers=headers, params=queryStringStats)

        text = response.text
        data = json.loads(text)
        return data["price"]["shortName"]