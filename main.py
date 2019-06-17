
import folium
import json
from requests_oauthlib import OAuth2Session

c_dict = {}
currencies = {"GBP": "£", "USD": "$", "EUR": "E"}
category_colour = {"shopping": "red", "groceries": "blue", "eating_out": "green", "entertainment": "purple",
                   "general": "lightred", "cash": "beige", "transport": "darkblue", "bills": "darkgreen",
                   "personal_care": "cadetblue", "holidays": "darkpurple"}
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
schemes = []
trannies = response["transactions"]
m = folium.Map(
    location=[51.583233, -0.101466],
    zoom_start=12,
    tiles='Stamen Terrain'
)
for tran in trannies:

    schemes.append(tran['is_load'])
    amount = int(tran['amount']) / -100
    currency = currencies.get(tran['currency'])
    if 'merchant' in tran:

        mer = tran["merchant"]
        if mer is not None:
            name = mer['name']
            if name == "Selale Restaurant":
                print(tran)
            category = mer['category']
            cat_list.append(category)
            if 'address' in mer:
                add = mer["address"]
                if 'latitude' in add and 'longitude' in add:
                    lat = add["latitude"]
                    long =add["longitude"]
                    pin_words = f'{name} - {category} - {currency}{amount:.2f}'
                    folium.Marker(location=[lat,long],zoom_start=12,popup=pin_words,
                                  icon=folium.Icon(color=category_colour.get(category))).add_to(m)

m.save("my_map_2.html")
