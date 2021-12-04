import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://api.billbee.io/api/v1/"
SERVICE = "products/stocks"

auth=HTTPBasicAuth('user', 'pass')


try:    
    print("Calling API... ", BASE_URL)
    response = requests.get(BASE_URL+SERVICE, auth=HTTPBasicAuth('user', 'pass'), headers={"X-Billbee-Api-Key":"4A021E4E-7FF2-466C-897B-D8BED482DF10"})
except Exception as e:
    print("ERROR: API call failed: ", e)

print(response.status_code, response.reason)