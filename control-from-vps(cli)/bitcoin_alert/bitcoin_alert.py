import requests
import conf
import time
import json
from boltiot import Bolt

mybolt = Bolt(conf.bolt_api_key, conf.device_id)

# Selling Price is in INR
selling_price = 800000

def get_bitcoin_price() :
	URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,INR&api_key= YOUR_API_KEY"      # Use the API Key provided on account creation at cryptocompare
	response = requests.request("GET",URL)
	response = json.loads(response.text)
	current_price = response["INR"]
	return current_price

def buzz() :
	response = mybolt.analogWrite('0','200')
	#print(response)
	time.sleep(5)
	response = mybolt.digitalWrite('0',"LOW")
	#print(response)

while True :
	current_price = get_bitcoin_price()
	if current_price > selling_price :
		buzz()
	time.sleep(30)


