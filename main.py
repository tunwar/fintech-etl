import gmplot
import json
from requests_oauthlib import OAuth2Session

c_dict = {}
currencies = {"GBP": "£", "USD": "$", "EUR": "E"}
category_colour = {"shopping": "aliceblue", "groceries": "beige", "eating_out": "red", "entertainment": "darkgray",
                   "general": "goldenrod", "cash": "lavender", "transport": "maroon", "bills": "ivory",
                   "personal_care": "lime", "holidays": "yellowgreen"}
with open(".env") as f:
    content = f.readlines()

for line in content:
    split_content = line.rstrip().split('=')
    c_dict[split_content[0]] = split_content[1]

token = {'access_token': c_dict['MONZO_TOKEN'],
         'token_type': 'Bearer'}
print(token)
sesh = OAuth2Session(token=token)
url = f'https://api.monzo.com/transactions?expand[]=merchant&account_id={c_dict["MONZO_ACC_ID"]}'

response = sesh.get(url).json()

#with open("out.json") as f:
#    response = json.load(f)

lats = []
longs = []
cat_list = []
trannies = response["transactions"]
gmap = gmplot.GoogleMapPlotter(51.583233, -0.101466, 10)
for tran in trannies:
    amount = int(tran['amount']) / -100
    currency = currencies.get(tran['currency'])
    if 'merchant' in tran:

        mer = tran["merchant"]
        if mer is not None:
            name = mer['name']
            category = mer['category']
            cat_list.append(category)
            if 'address' in mer:
                add = mer["address"]
                if 'latitude' in add and 'longitude' in add:
                    lat = add["latitude"]
                    long =add["longitude"]
                    pin_words = f'{name} - {category} - {currency}{amount:.2f}'
                    gmap.marker(lat,long, category_colour.get(category),title=pin_words)

print(list(dict.fromkeys(cat_list)))

# gmap.heatmap(lats, longs)



gmap.draw("my_map.html")
