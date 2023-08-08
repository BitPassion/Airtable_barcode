from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np  # Import NumPy

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
