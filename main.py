import os
import time
from gui import GUI
import requests
from twilio.rest import Client

# API/Environmental Variable Constants
API_KEY = os.environ.get("API_KEY_TWL")

API_KEY_TWL = os.environ.get("TWL_AUTH_TOKEN")
TWL_SMS = os.environ.get("TWL_NUMBER")
TWL_SID = os.environ.get("TWL_SID")

endpoint = "https://api.priceapi.com/v2/jobs"
job_id: str
success = False

# Forces user to keep entering a valid product (very unlikely)
while success is False:
    gui = GUI()
    parameters = {
        "token": API_KEY,
        "source": "amazon",
        "country": "us",
        "topic": "search_results",
        "key": "term",
        "values": gui.values,
        "max_pages": "1",
        "max_age": "1440"
    }
    response = requests.post(url=endpoint, json=parameters)
    try:
        success = response.json()["success"]
        if success is False:
            gui.failed()
    except KeyError:
        job_id = response.json()["job_id"]
        success = True

gui.succeed()
# API requires some time to gather the data so the code needs to wait
time.sleep(7)

parameters = {
    "token": API_KEY,
    "job_id": job_id
}

endpoint = f"https://api.priceapi.com/v2/jobs/{job_id}/download"
response = requests.get(url=endpoint, params=parameters)

# Compiles the data into a dictionary and finds the lowest prices and the corresponding URL
data_results = response.json()["results"][0]["content"]["search_results"]

data = {result["min_price"]: result["url"] for result in data_results}

best_deals = [float(price) for price in data.keys() if price is not None]
best_deals.sort()

# Creates the message with the best deals and their URLs
summarized_data = ""
for x in range(0, len(best_deals) if len(best_deals) < 10 else 10):
    summarized_data += f"${best_deals[x]} : {data[str(best_deals[x])]}\n"

# Sends the message
client = Client(TWL_SID, API_KEY_TWL)
message = client.messages \
    .create(
    body=summarized_data,
    from_=TWL_SMS,
    to=""+os.environ.get("PHONE_NUMBER")
)

print(message.status)
