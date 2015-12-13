# -*- coding: utf-8 -*-
"""
Created on Tue Dec 08 16:59:54 2015

@author: Renato

Program written in Python 2.7. This program transforms pdf files into html ones. 
Simply run the program and choose the folder where the pdf files you want to transform are stored. 
The program will transform all pdf files that it finds in that folder and subfolders and will ignore non-pdf files. 
The program also deltes useless tags with no information that are created when the images from the pdf are transformed. 
The html files are stored on the same location as the pdf files with the same name but with the .html extension.
"""

import Tkinter, tkFileDialog
import os
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    strng = retstr.getvalue()
    retstr.close()
    return strng


def main():
  
    root = Tkinter.Tk()
    root.withdraw()
    dirname = tkFileDialog.askdirectory(parent=root,initialdir="C:\\",title='Please select a directory')
    if len(dirname ) > 0:
        for root, dirs, filenames in os.walk(dirname):
            for fn in filenames:
                if os.path.splitext(fn)[1] == ".pdf":
                    html_code=convert_pdf_to_html(dirname+"\\"+fn)
                    html_code_filtered = re.sub('<span.*?></span>', '', html_code)
                    html_file = open(dirname+"\\"+os.path.splitext(fn)[0]+".html", "w")
                    html_file.write(html_code_filtered)
                    html_file.close()                
         


if __name__ == '__main__':
    main() 
