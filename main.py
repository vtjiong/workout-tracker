import requests
from datetime import datetime
import os

# Fetch environment variables
application_id = os.getenv('APP_ID')
application_key = os.getenv('APP_KEY')
sheety_endpoint = os.getenv('sheety')
sheety_token = os.getenv('token')

# Nutritionix API endpoint and headers
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutritionix_headers = {
    'x-app-id': application_id,
    'x-app-key': application_key,
    'x-remote-user-id': "0"
}

# Collect user input for exercises
exercise_query = input("Tell me which exercises you did: ")

# Parameters for the exercise query
parameters = {
    "query": exercise_query,
    "gender": "Male",
    "weight_kg": 105,
    "height_cm": 186,
    "age": 21
}

# Make a POST request to the Nutritionix API
response = requests.post(url=nutritionix_endpoint, headers=nutritionix_headers, json=parameters)

# Check if the request was successful
if response.status_code == 200:
    result = response.json().get("exercises", [])
    print(result)
else:
    print("Failed to retrieve exercises from Nutritionix API.")
    result = []

# Headers for Sheety API
sheety_headers = {
    "Authorization": f"Bearer {sheety_token}"
}

# Post each exercise to Sheety
for exercise in result:
    workout = {
        "sheet1": {
            "date": datetime.now().strftime("%m/%d/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Make a POST request to the Sheety API
    sheety_response = requests.post(url=sheety_endpoint, json=workout, headers=sheety_headers)

    # Check if the request was successful
    if sheety_response.status_code == 200:
        print("Exercise logged successfully:", workout)
    else:
        print("Failed to log exercise to Sheety:", workout)

# Note:
# response.json() parses the response from strings to a valid JSON data structure,
# while response.text provides the raw string data.
