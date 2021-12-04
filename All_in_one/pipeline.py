import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class Google_Sheets:

    def __init__(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.

        creds = None
        scopes = ['https://www.googleapis.com/auth/spreadsheets']

        if os.path.exists('keys/token.json'):
            creds = Credentials.from_authorized_user_file('keys/token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'keys/credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('keys/token.json', 'w') as token:
                token.write(creds.to_json())

        # Creating Service as Instance Attribute
        self.SERVICE = build('sheets', 'v4', credentials=creds)


    def write_pandas_to_sheet(self, df, spreadsheet_id, include_headers=True):

        headers = [list(df.columns)] if include_headers else []
        values = headers + df.values.tolist()
        body = {'values': values}

        resultClear = self.SERVICE.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id, range='!A1:Z',
                body={}).execute()
        print(f"Cleared {resultClear.get('clearedRange')} for Google Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        result = self.SERVICE.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range='A1',
                valueInputOption='USER_ENTERED', body=body).execute()
        print(f"Updated {result.get('updatedCells')} cells for Google Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    

GOOGLE_SHEETS = Google_Sheets()


import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://api.billbee.io/api/v1/"
AUTH = HTTPBasicAuth('info@manisma.com', '5EHLf3BLj6xQaqz')
HEADERS = {"X-Billbee-Api-Key":"4A021E4E-7FF2-466C-897B-D8BED482DF10"}

def call_billbee(service):
    try:    
        print("Calling API... ", BASE_URL)
        response = requests.get(BASE_URL+service, auth=AUTH, headers=HEADERS)
    except Exception as e:
        print("ERROR: API call failed: ", e)

    print(response.status_code, response.reason)

    return response.json()

def extract_shipping(ShippingIds):
    shipping = {
    "ShippingId": "",
    "Shipper": "",
    "TrackingUrl": ""
    }
    for ship in ShippingIds:
        for att in shipping:
            if ship.get(att, None):
                shipping[att] = ship[att]
    return shipping

def extract_adress(adress):
    adr = ""
    for loc in ["FirstName", "LastName", "Street", "HouseNumber", "Zip", "City", "Country"]:
        adr += adress[loc] + " "
    return adr

def extract_product(products):
    product_lists = {k: [] for k in ["Product", "Quantity", "TotalPrice", "ProductWeight", "ProductBillbeeId"]}
    for product in products:
        product_lists["Product"].append(product["Product"]["Title"])
        product_lists["ProductWeight"].append(product["Product"]["Weight"])
        product_lists["ProductBillbeeId"].append(product["Product"]["BillbeeId"])
        product_lists["Quantity"].append(product["Quantity"])
        product_lists["TotalPrice"].append(product["TotalPrice"])
    return product_lists





SPREADSHEET_ID = '1jre8imIUz61QqArOqwYCrRF5JXuKZ1dv-ub1U-SU8uo'

json_data = call_billbee("orders")
data = json_data['Data']

df = pd.DataFrame(data)
df = df.fillna('')

shipping_df = df["ShippingIds"].apply(extract_shipping).apply(pd.Series)
df = pd.concat([shipping_df, df], axis=1)
seller_df = df["Seller"].apply(lambda x: {key: x[key] for key in ['Platform', 'BillbeeShopName', 'BillbeeShopId']}).apply(pd.Series)
df = pd.concat([df, seller_df], axis=1)
customer_df = df["Customer"].apply(lambda x: {"Customer" + key: x[key] for key in ['Id', 'Name', 'Email']}).apply(pd.Series)
df = pd.concat([df, customer_df], axis=1)
product_df = df["OrderItems"].apply(extract_product).apply(pd.Series)
product_df = pd.concat([df["Id"], product_df], axis=1)
product_df = product_df.set_index("Id").apply(pd.Series.explode).reset_index()
df = df.merge(product_df, on='Id', how='inner')

df["InvoiceAddress"] = df["InvoiceAddress"].apply(extract_adress)
df["ShippingAddress"] = df["ShippingAddress"].apply(extract_adress)
df["Tags"] = df["Tags"].apply(lambda tags:", ".join(tags))

drops = ["ShippingIds", "SellerComment", "Comments", "InvoiceAddress", "ShippingAddress", "OrderItems", "ShippingAddress", "OrderItems", "Seller", "Customer", "Payments", "History"]
df = df.drop(columns=drops)

print(df)

GOOGLE_SHEETS.write_pandas_to_sheet(df, SPREADSHEET_ID)