from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import requests
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload  
from airtable import Airtable


def add_to_airtable(api_key, base_id, table_name, barcode_value, pdf_link):
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Doctor Form Upload": [
                {
                    "url": pdf_link
                }
            ],
            "Barcode": {
                "text": barcode_value[:-1]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Barcode added to Airtable successfully!")
    else:
        print(f"Failed to add to Airtable. Status code: {response.status_code}. Response: {response.text}")

def upload_file_to_folder(filename, filepath, mimetype, folder_id):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")

    # Make the file shareable
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file.get('id'), body=permission, fields='id').execute()

    # Get the shareable link
    link = f"https://drive.google.com/file/d/{file.get('id')}/view?usp=drive_link"
    return link

def update_to_airtable(api_key, base_id, table_name, barcode_value, pdf_link, id):
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "records": [
            {
            "id": id,
            "fields": {
    
                "Doctor Form Parsed/Upload": [
                {
                    "url": pdf_link
                }
                ],
            }
            }
        ]
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Barcode added to Airtable successfully!")
    else:
        print(f"Failed to add to Airtable. Status code: {response.status_code}. Response: {response.text}")

# Store Pdf with convert_from_path function
images = convert_from_path('output.pdf', poppler_path=r'C:\Program Files\poppler\bin')

im = images[1]
width, height = im.size

# Setting the points for cropped image
left = 1370
top = 1920
right = 1630
bottom = 2060

# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))

# Shows the image in image viewer
# im1.show()

# Convert PIL image to NumPy array
im1_np = np.array(im1)

def barcodeReader(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    barcodes = decode(gray_img)
    return barcodes[0].data.decode('utf-8')

barcode = barcodeReader(im1_np)
print(barcode[:-1])

# Replace with your Airtable API credentials and base ID
API_KEY = 'patsKa7ue00yT7O5z.8c6a89bca50e9a991b71477388b597d968ef4b2d79edbd8edf3e18a1d8bfdb7f'
BASE_ID = 'app9TEsn6f0IFjNup'
TABLE_NAME = 'tblUha0m2h1hGDF3A'

# Initialize the Airtable client
airtable1 = Airtable(BASE_ID, TABLE_NAME, api_key=API_KEY)

# Retrieve all records from the table
all_records = airtable1.get_all()

# Extract barcode values from each record
barcode_values = []

for record in all_records:
    barcode_field = record['fields'].get('Barcode')
    if barcode_field and barcode_field.get('text') == barcode[:-1]:
        name = record['fields'].get('Name', '')
        record_id = record['id']

        print(f"Record ID: {record_id}")
        print(f"Name: {name}")
        print("----------")
        break
#-----------------------------------------------------------

# Load the Service Account's credentials
SERVICE_ACCOUNT_FILE = 'credential.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive API client
service = build('drive', 'v3', credentials=credentials)

# Example: Upload a file
FOLDER_ID = '1_wjHSlUFazrJh0nWOtPVHTebM7VpaBGg'
pdf_link = upload_file_to_folder('completed' + barcode + '.pdf', 'D:\Barcode_airtable\Airtable_barcode\output.pdf', 'application/pdf', FOLDER_ID)
print(f"Shareable link: {pdf_link}")

# Add barcode to Airtable
update_to_airtable(API_KEY, BASE_ID, TABLE_NAME, barcode, pdf_link, record_id)