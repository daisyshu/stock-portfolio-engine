import http.client

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
    }

conn.request("GET", "/market/get-summary?region=US&lang=en", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))