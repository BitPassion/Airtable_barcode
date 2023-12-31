#Extract data from pdf file.

from PyPDF2 import PdfReader

infile = "output.pdf"

pdf_reader = PdfReader(open(infile, "rb"))


with open('result.csv','w') as resultcsv:

    dictionary = pdf_reader.get_fields(fileobj = resultcsv)

textfields = pdf_reader.get_form_text_fields()

dest = pdf_reader.named_destinations

print(dest)