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

import logging
import logging.handlers
import os

log_directory = "/var/logs/gsheets"
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger('gsheets')
logger.setLevel(logging.INFO)

handler = logging.handlers.TimedRotatingFileHandler(
    filename=os.path.join(log_directory, 'gsheets.log'),
    when="W6",
    interval=1,
    backupCount=4
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


##### LINK ####
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update?apix_params=%7B%22spreadsheetId%22%3A%221YqE0q4yaWE4AtJbbyEAOmvANqtuBMJnxh6NT3Mw9DFg%22%2C%22range%22%3A%227A!E16%22%2C%22valueInputOption%22%3A%22USER_ENTERED%22%2C%22resource%22%3A%7B%22values%22%3A%5B%5B12%5D%5D%7D%7D

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



def query_influxdb_last_record(url, database, username, password, measurement):
    # Define the InfluxQL query
    query = f'SELECT * FROM {measurement} ORDER BY time DESC LIMIT 1'

    # Define the request parameters
    params = {
        'db': database,
        'q': query
    }

    # Send GET request to the InfluxDB server with authentication
    response = requests.get(url, params=params, auth=(username, password))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the results
        results = data['results']

        # Check if there are any query results
        if len(results) > 0 and 'series' in results[0]:
            series = results[0]['series'][0]

            # Extract the column names and values
            columns = series['columns']
            values = series['values'][0]

            # Create variables and assign values
            variables = {}
            for i, column in enumerate(columns):
                variables[column] = values[i]

            return variables
        else:
            logger.info('No data found for the query.')
    else:
        logger.info('Error:', response.status_code)







def push_gsheets(range_cell, val):
    logger.info(f"range-->{range_cell}")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/app/token.json'):
        creds = Credentials.from_authorized_user_file('/app/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/app/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/app/token.json', 'w') as token:
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





# Define the InfluxDB server URL and database name
url = 'http://influxdb.docker.local:8086/query'
database_idb = 'ph'
username = 'pi'
password = 'raspberry'
measurement = 'vat1'
base_idx = int(os.environ.get('BASE_IDX', 16)) # Default to 16 if not set ----->starting index for the target Google sheet
count = 0


while True:
    # Query the last record
    result = query_influxdb_last_record(url, database_idb, username, password, measurement)


    # Print the retrieved data Influxdb data
    if result:
        timestamp_i = result['time']
        temp_i = result['temp']
        ph_i = result['ph']
        # threshold_i = result['threshold']
        
        logger.info(f"Timestamp: {timestamp_i}")
        logger.info(f"Temperature: {temp_i}")
        logger.info(f"pH: {ph_i}")
        # print("Threshold:", threshold_i)
        date_i, time_i = timestamp_i.split("T")
        time_i = time_i.split("Z")[0]# print(datetime.datetime.fromtimestamp(int(t1)).strftime('%H:%M'))
        # logger.info(time_i)

        

        push_gsheets('7A!E'+str(base_idx),round(ph_i,2))
        push_gsheets('7A!C'+str(base_idx), time_i)
        push_gsheets('7A!B'+str(base_idx), date_i)
        
        machine_name="vat1"
        count+=1
        base_idx+=1 #------------> increment Google sheet rows

        var = "curl -i -XPOST 'http://influxdb.docker.local:8086/write?db=ph' --data '"+machine_name+" status="+str(count)+"'"
        os.system(var)
        time.sleep(1800)





