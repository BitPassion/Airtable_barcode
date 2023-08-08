# import module
from pdf2image import convert_from_path
# Importing Image class from PIL module
from PIL import Image
 
 
# Store Pdf with convert_from_path function
images = convert_from_path('output.pdf', poppler_path = r'C:\Program Files\poppler\bin')
 
# for i in range(len(images)):
   
#       # Save pages as images in the pdf
#     images[i].save('page'+ str(i) +'.jpg', 'JPEG')

images[1].save('captured.jpg','JPEG')


# Opens a image in RGB mode
im = Image.open(r"captured.jpg")
# im = images[1].save('captured.jpg','JPEG')
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
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
im1.show()