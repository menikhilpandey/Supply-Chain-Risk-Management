from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import nltk
import  nltk.data
from nltk import tokenize
from nltk.tokenize import sent_tokenize
import numpy as np
import pandas as pd


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def removeNonAscii( text):

    return ''.join([i if ord(i) < 128 else ' ' for i in text]) 
    

def convert(fname, pages=None, WindowSize=1 ):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    
    
    output.close
    #text="Its been so long. I havent seen your face. i am tryin to be strong. but the strength i have is washing away."
    
    
    
    sent_list = sent_tokenize(removeNonAscii(text).replace('\n', ' ') )
    
    #sent_list = text.splitlines()
    
    
#     df = pd.DataFrame(sent_list , columns=["sentence"])
#     #df.iloc[::n,:]
#     print df["sentence"][0]
#     print df["sentence"][1]
#     print df["sentence"][2]
#     print df["sentence"][3]
#     print df["sentence"][4]
#     
#     print "We did it !!!"
    
    sentenceListOut=[]
    
    # n refers to size of each window.
    n=WindowSize
    
    
    i=0
    while ( i < len(sent_list) and n>1):
        sentenceListOut.append(" ".join(sent_list[i:i+n]))
        i=i+n+1
        
    #print sentenceListOut[0]
    
    
    df = pd.DataFrame(sent_list , columns=["sentence"])
    #print sent_list[4]
    #print "We did it !!!"
    df.to_csv("sample.csv", mode='w')
    return text 


convert('fm.pdf', pages=None , WindowSize = 1)