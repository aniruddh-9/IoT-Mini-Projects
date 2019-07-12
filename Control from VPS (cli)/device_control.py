from boltiot import Bolt
api_key="dc29855b-44ed-4781-af5d-e9087ed4b597"
device_id="BOLT1115914"
mybolt = Bolt(api_key,device_id)
response = mybolt.restart()
print(response)
