import requests
from datetime import datetime
import os
application_id= f"{os.environ.get('APP_ID')}"
application_key = f"{os.environ.get('APP_KEY')}"
endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    'x-app-id' : application_id,
    'x-app-key': application_key,
    'x-remote-user-id': "0"
}
parameters = {
    "query": input("Tell me which exercises you did: "),
    "gender": "Male",
    "weight_kg": "105",
    "height_cm": "186",
    "age": 21
}
response = requests.post(url=endpoint, headers=headers, json=parameters)
result = response.json()["exercises"]
print(result)
sheety_endpoint=f"{os.environ.get('sheety')}"
headers = {
    "Authorization": f"Bearer {os.environ.get('token')}"
}
for x in result:
    workout = {
       "sheet1": {
            "date":datetime.now().strftime("%m/%d/%Y"),
            "time":datetime.now().strftime("%H:%M:%S"),
            "exercise":x["name"].title(),
            "duration":x["duration_min"],
            "calories":x["nf_calories"]
        }
    }
    response = requests.post(url=sheety_endpoint, json=workout,headers=headers)
# response.json() parses the response from strings to a valid json data structure using a lists and stuff,
# while response.text is still a string