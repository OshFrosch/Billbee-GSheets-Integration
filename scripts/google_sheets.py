from __future__ import print_function
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