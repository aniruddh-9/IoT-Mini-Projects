import sms_conf
from boltiot import Sms,Bolt
import json,time

minimum_limit = 300
maximum_limit = 600

mybolt = Bolt(sms_conf.API_KEY,sms_conf.DEVICE_ID)
sms = Sms(sms_conf.SID,sms_conf.AUTH_TOKEN,sms_conf.TO_NUMBER,sms_conf.FROM_NUMBER)

while True:
	print("Reading Sensor Value");
	response = mybolt.analogRead('A0')
	data=json.loads(response)
	print("Sensor value : " + str(data['value']))
	try:
		sensor_value=int(data['value'])
		if sensor_value  >maximum_limit or sensor_value<minimum_limit:
			print("Making request to Twilio for SMS")
			response = sms.send_sms("The Current Temperature : "+str(sensor_value))
			print("Status of SMS at Twilio : "+ str(response.status))
	except Exception as e:
		print("Error occured: Below are the details")
		print(e)
	time.sleep(10)


