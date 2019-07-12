import requests
import conf
import time
import json
from boltiot import Bolt

mybolt = Bolt(conf.bolt_api_key, conf.device_id)

# Selling Price is in INR
selling_price = 800000

def get_bitcoin_price() :
	URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,INR&api_key=c8d6bf1d54c80571dd4c0f30bd3430df4b2b6c56e7cf795bf2164aad1c2e3843"
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


