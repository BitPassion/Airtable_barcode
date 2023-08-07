#generate barcode, upload to airtable.

import random
from barcode import EAN13
from barcode.writer import ImageWriter
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.lib.units import mm
import os
import requests

def generate_random_ean13():
    # Generate a random 12-digit number for the EAN13 barcode
    random_number = "".join([str(random.randint(0, 9)) for _ in range(12)])

    # Now, let's create an object of EAN13
    # Set the 'humanReadable' property in ImageWriter options
    writer_options = {'write_text': False}
    writer = ImageWriter()
    writer.set_options(writer_options)
    
    # class and pass the number
    my_code = EAN13(random_number, writer=writer)
    
    # Our barcode is ready. Let's save it.
    my_code.save("barcode_img", options={"write_text": False})
    return random_number

def create_barcode_page(output_filename, barcode_value):
    # Create a new PDF with Reportlab that contains the barcode
    packet = BytesIO()
    barcode = createBarcodeDrawing('EAN13', value=barcode_value, barHeight=40*mm, humanReadable=False)
    c = canvas.Canvas(packet, pagesize=letter)
    barcode_width, barcode_height = barcode.width, barcode.height
    x_position = (c._pagesize[0] - barcode_width) // 2
    y_position = (c._pagesize[1] - barcode_height) // 2
    renderPDF.draw(barcode, c, x_position, y_position)
    c.save()
    
    packet.seek(0)
    new_pdf = PdfReader(packet)
    return new_pdf

def create_image_page(image_path):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)  # assuming landscape, modify as needed

    # Add image to canvas. Modify x, y, width, and height as needed.
    c.drawImage(image_path, 100, 100)

    c.showPage()
    c.save()
    
    packet.seek(0)
    return PdfReader(packet)

def add_barcode_to_pdf(input_filename, output_filename, barcode_value):
    original = PdfReader(input_filename)
    output = PdfWriter()
    
    # Add original PDF pages
    for page in original.pages:
        output.add_page(page)
    
    # Create a new page with barcode
    barcode_page = create_barcode_page(output_filename, barcode_value)
    output.add_page(barcode_page.pages[0])

    # Add image page
    image_page = create_image_page("barcode_img.png")
    output.add_page(image_page.pages[0])
    
    # Write the output to a new file
    with open(output_filename, "wb") as output_pdf_file:
        output.write(output_pdf_file)

def add_to_airtable(api_key, base_id, table_name, barcode_value):
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Barcode Image": [
                {
                    "url": "D:/Parse_pdf_barcode/barcode_img.png"
                }
            ],
            "Barcode": {
                "text": barcode_value
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Barcode added to Airtable successfully!")
    else:
        print(f"Failed to add to Airtable. Status code: {response.status_code}. Response: {response.text}")

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    input_pdf = os.path.join(directory, "input.pdf")
    output_pdf = os.path.join(directory, "output.pdf")
    barcode_value = generate_random_ean13()

    add_barcode_to_pdf(input_pdf, output_pdf, barcode_value)
    print(f"Barcode {barcode_value} added and saved as output.pdf")

    # Airtable credentials
    API_KEY = "patsKa7ue00yT7O5z.ab8ac81f77631852c08df2c18fec20e0b8785126f563f23a6b47e10e70082c58"
    BASE_ID = "app9TEsn6f0IFjNup"
    TABLE_NAME = "tblUha0m2h1hGDF3A"

    # Add barcode to Airtable
    add_to_airtable(API_KEY, BASE_ID, TABLE_NAME, barcode_value)