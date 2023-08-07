from pyzbar.pyzbar import decode
import cv2

def barcodeReader(url):
    image = cv2.imread(url)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)
    return barcodes[0].data.decode('utf-8')

barcode = barcodeReader("barcode_img.png")
print (barcode)