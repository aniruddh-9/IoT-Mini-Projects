import conf,json,requests,math,statistics
import time
from boltiot import Bolt

PARAMS={'status': "undefined"}

def trigger_integromat_webhook(state):
	PARAMS['status']=state
	URL = conf.INTEGROMAT_URL
	response = requests.get(URL, PARAMS)
	print (response.text)

def compute_bounds(history_data,frame_size,factor) :
	if(len(history_data)<frame_size) :
		return None
	if(len(history_data)>frame_size) :
		del history_data[0:len(history_data)-frame_size]
	Mn=statistics.mean(history_data)
	Variance=0
	for data in history_data :
		Variance += math.pow((data-Mn),2)
	Zn = factor * math.sqrt(Variance / frame_size)
	High_bound = history_data[frame_size-1]+Zn
	Low_bound = history_data[frame_size-1]-Zn
	return [High_bound,Low_bound]

mybolt = Bolt(conf.API_KEY,conf.DEVICE_ID)
history_data=[]

while True:
	response = mybolt.analogRead('A0')
	data = json.loads(response)
	if data['success'] != 1:
		print("There was an error whilst retrieving the data")
		print("This is the value" + data['value'])
		time.sleep(10)
		continue
	print("This is the value: "+ data['value'])
	sensor_value=0
	try:
		sensor_value = int(data['value'])
	except e:
		print("There was an error while parsing the response: ",e)
		continue
	
	bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
	if not bound:
		required_data_count = conf.FRAME_SIZE-len(history_data)
		print("Not enough data to compute Z-Score. Need ",required_data_count, "more data points")
		history_data.append(int(data['value']))
		time.sleep(10)
		continue
	try:
		if sensor_value > bound[0]:
			trigger_integromat_webhook("ON")
		#	PARAMS['status']="ON"
		elif sensor_value < bound[1]:
			trigger_integromat_webhook("OFF")
		#	PARAMS['status']="OFF"
		history_data.append(sensor_value)
	except Exception as e:
		print("Error",e)
	time.sleep(10)

