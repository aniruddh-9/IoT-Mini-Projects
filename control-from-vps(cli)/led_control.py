from boltiot import Bolt
api_key="YOUR_API_KEY"
device_id="YOUR_DEVICE_ID"
mybolt = Bolt(api_key,device_id)
response = mybolt.digitalWrite('0','HIGH')
print(response)
