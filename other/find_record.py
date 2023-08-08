#find the record which barcode in matches to the pdf file

import requests

# Your Airtable setup
API_KEY = 'patsKa7ue00yT7O5z.ab8ac81f77631852c08df2c18fec20e0b8785126f563f23a6b47e10e70082c58'
BASE_ID = 'app9TEsn6f0IFjNup'
TABLE_NAME = 'tblUha0m2h1hGDF3A'
COLUMN_NAME = 'Barcode'
SEARCH_VALUE = '1234567890123'

endpoint = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Build the query string
params = {
    'filterByFormula': f'{{ {COLUMN_NAME} }} = "{SEARCH_VALUE}"'
}

response = requests.get(endpoint, headers=headers, params=params)

if response.status_code == 200:
    records = response.json().get('records')
    if records:
        for record in records:
            print(record)
    else:
        print(f'No records found with {COLUMN_NAME} = {SEARCH_VALUE}')
else:
    print(f"Failed with status code: {response.status_code}")
