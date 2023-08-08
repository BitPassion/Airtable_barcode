# import fitz
# import io
# from PIL import Image
  
# # STEP 2
# # file path you want to extract images from
# file = "output.pdf"
  
# # open the file
# pdf_file = fitz.open(file)
  
# # STEP 3
# # iterate over PDF pages
# for page_index in range(len(pdf_file)):
  
#     # get the page itself
#     page = pdf_file[page_index]
#     image_list = page.getImageList()
  
#     # printing number of images found in this page
#     if image_list:
#         print(
#             f"[+] Found a total of {len(image_list)} images in page {page_index}")
#     else:
#         print("[!] No images found on page", page_index)
#     for image_index, img in enumerate(page.getImageList(), start=1):
  
#         # get the XREF of the image
#         xref = img[0]
  
#         # extract the image bytes
#         base_image = pdf_file.extractImage(xref)
#         image_bytes = base_image["image"]
  
#         # get the image extension
#         image_ext = base_image["ext"]




# import module
from pdf2image import convert_from_path
 
 
# Store Pdf with convert_from_path function
images = convert_from_path('output.pdf', poppler_path = r'C:\Program Files\poppler\bin')
 
# for i in range(len(images)):
   
#       # Save pages as images in the pdf
#     images[i].save('page'+ str(i) +'.jpg', 'JPEG')

images[1].save('captured.jpg','JPEG')
