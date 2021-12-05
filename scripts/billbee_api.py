import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://api.billbee.io/api/v1/"
AUTH = HTTPBasicAuth('info@manisma.com', '******')
HEADERS = {"X-Billbee-Api-Key":"******"}

def call_billbee(service):
    try:    
        print("Calling API... ", BASE_URL)
        response = requests.get(BASE_URL+service, auth=AUTH, headers=HEADERS)
    except Exception as e:
        print("ERROR: API call failed: ", e)

    print(response.status_code, response.reason)

    return response.json()
