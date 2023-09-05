from pprint import pprint

from googleapiclient import discovery
import requests
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import time
from datetime import datetime





##### LINK ####
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update?apix_params=%7B%22spreadsheetId%22%3A%221YqE0q4yaWE4AtJbbyEAOmvANqtuBMJnxh6NT3Mw9DFg%22%2C%22range%22%3A%227A!E16%22%2C%22valueInputOption%22%3A%22USER_ENTERED%22%2C%22resource%22%3A%7B%22values%22%3A%5B%5B12%5D%5D%7D%7D

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']




def push_gsheets(range_cell, val):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to update.
    spreadsheet_id = '1YqE0q4yaWE4AtJbbyEAOmvANqtuBMJnxh6NT3Mw9DFg'  # TODO: Update placeholder value.

    # The A1 notation of the values to update.
    range_ = range_cell  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    value_range_body = {
        # TODO: Add desired entries to the request body. All existing entries
        # will be replaced.
        "values": [
        [
        val
        ]
    ]
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()


    # TODO: Change code below to process the `response` dict:
    pprint(response)





base_idx = int(os.environ.get('BASE_IDX', 16)) # Default to 16 if not set ----->starting index for the target Google sheet
count = 0


while True:
        
    push_gsheets('7A!E'+str(base_idx), "activated")
    push_gsheets('7A!C'+str(base_idx), "activated")
    push_gsheets('7A!B'+str(base_idx), "activated")
        






