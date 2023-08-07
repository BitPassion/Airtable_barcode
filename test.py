#Extract data from pdf file not good.

from PyPDF2 import PdfReader
from pprint import pprint
pdf_file_name = 'input.pdf'

f = PdfReader(pdf_file_name)
fields = f.get_fields()
print('RESULT : ', fields)
fdfinfo = dict((k, v.get('/V', '')) for k, v in fields.items())
pprint(fdfinfo)

with open('test.csv', 'w') as f2:
    for key in fdfinfo.keys():
        if type(key)==type("string") and type(str(fdfinfo[key]))==type("string"):
            f2.write('"'+key+'","'+fdfinfo[key]+'"\n')