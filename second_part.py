from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np  
from airtable import Airtable

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
print(barcode)

# Replace with your Airtable API credentials and base ID
API_KEY = 'patsKa7ue00yT7O5z.ab8ac81f77631852c08df2c18fec20e0b8785126f563f23a6b47e10e70082c58'
BASE_ID = 'app9TEsn6f0IFjNup'
TABLE_NAME = 'tblUha0m2h1hGDF3A'

# Initialize the Airtable client
airtable = Airtable(BASE_ID, TABLE_NAME, api_key=API_KEY)

# Retrieve all records from the table
all_records = airtable.get_all()

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