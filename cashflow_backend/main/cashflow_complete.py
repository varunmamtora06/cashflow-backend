#!/usr/bin/env python
# coding: utf-8

# In[62]:


from PIL import Image
import pytesseract
import cv2
import os
import pandas as pd
import numpy as np
import csv
import re
import string
from glob import glob
import warnings
warnings.filterwarnings('ignore')



#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = r'../cashflow_backend/Tesseract-OCR/tesseract'


# In[66]:




# In[ ]:





# In[ ]:





# In[69]:
def predictIMG(img):

    def cleanText(txt):
        whitespace = string.whitespace
        punctuation = "!#$%&\'()*+:;<=>?[\\]^`{|}~"
        tableWhitespace = str.maketrans('','',whitespace)
        tablePunctuation = str.maketrans('','',punctuation)
        text = str(txt)
        #text = text.lower()
        removewhitespace = text.translate(tableWhitespace)
        #removepunctuation = removewhitespace.translate(tablePunctuation)

        return str(removewhitespace)

    class groupgen():
        def __init__(self):
            self.id = 0
            self.text = ''

        def getgroup(self,text):
            if self.text == text:
                return self.id
            else:
                self.id +=1
                self.text = text
                return self.id


    # In[70]:


    tessData = pytesseract.image_to_data(img).lower()
    # convert into dataframe
    tessList = list(map(lambda x:x.split('\t'), tessData.split('\n')))
    df = pd.DataFrame(tessList[1:],columns=tessList[0])
    df.dropna(inplace=True) # drop missing values
    df['text'] = df['text'].apply(cleanText)

    # convet data into content
    df_clean = df.query('text != "" ')
    content = " ".join([w.lower() for w in df_clean['text']])
    #print(content)


    # In[71]:


    text=(pytesseract.image_to_string(img)).lower()
    #print(text)
    def Convert(string):
        li = list(string.split("\n"))
        return li

    # Driver code    

    #print(Convert(text))
    dataName = Convert(text)
    dataN = []
    test_list = []
    for i in dataName:
        j = i.replace(' ','')
        dataN.append(j)

    dataN = [i for i in dataN if i]
    mer_name = dataN[0:2]
    mer_name


    # In[72]:


    date = []


    # In[73]:


    d1 = re.findall(r"([\d]{1,2}\s(?:jan|nov|oct|dec)\s[\d]{4})", content)
    d1


    # In[74]:


    d2 = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{2}", content)
    d2


    # In[75]:


    d3 = re.findall(r"[\d]{1,2}-[\d]{1,2}-[\d]{4}", content)
    d3


    # In[76]:


    if d1:
        date = d1
    if d2:
        date = d2
    if d3:
        date = d3
    if date:    
        date = date[0]


    # In[77]:


    df.dropna(inplace=True) # drop the missing in rows
    col_int = ['level','page_num','block_num','par_num','line_num','word_num','left','top','width','height']
    df[col_int] = df[col_int].astype(int)
    df['conf'] = df['conf'].astype(float)
    col_int = ['conf']
    df[col_int] = df[col_int].astype(int)
    #df.info()


    # In[78]:


    amount_words = ['cash','amt','total','amount','amt:','grand','total:','[amount','(total:','value','mrp/rate','222.46']
    cash = df[df['text'].isin(amount_words)]
    cash


    # In[79]:


    image = img.copy()
    level = 'word'
    a = 0
    for l,x,y,w,h,c,txt in cash[['level','left','top','width','height','conf','text']].values:
        #print(l,x,y,w,h,c)
        if level == 'page':
            if l == 1:
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)
            else:
                continue

        elif level == 'word':
            if l == 5:
                img4 = image.copy()
                #cv2.rectangle(image,(x-15,y-15),(x+w+10000,y+h+100),(0,255,0),2)
                img3= cv2.rectangle(img4,(x-5,y-5),(x+w+10000,y+h+100),(0,255,0),2)
                #cv2.putText(image,txt,(x,y),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                roi = image[y-5:y+h+100, x:x+w+10000]
                cv2.imwrite("../cashflow_backend/main/test_img/roi"+str(a)+'.jpeg', roi)
            else:
                continue

        a+=1



    # In[80]:


    dL = []
    path = "../cashflow_backend/main/test_img/"
    files = folders = 0

    for _, dirnames, filenames in os.walk(path):
    # ^ this idiom means "we won't be using this value"
        files += len(filenames)
        folders += len(dirnames)

    # print("{:,} files, {:,} folders".format(files, folders))
    imgs_in_folder = files
    # print(imgs_in_folder)
    # In[81]:


    for i in range(imgs_in_folder):
        img = cv2.imread('../cashflow_backend/main/test_img/roi'+str(i)+'.jpeg')
        tessData = pytesseract.image_to_data(img).lower()
    # convert into dataframe
        tessList = list(map(lambda x:x.split('\t'), tessData.split('\n')))
        df = pd.DataFrame(tessList[1:],columns=tessList[0])
        df.dropna(inplace=True) # drop missing values
        df['text'] = df['text'].apply(cleanText)

        # convet data into content
        df_clean = df.query('text != "" ')
        content = " ".join([w.lower() for w in df_clean['text']])
        #print(content)

        dL.append(content)
    #print(text)
    dL


    # In[82]:


    dat_re = re.compile(r'\d+\.\d+')
    dat_list = [float(dat_re.search(x).group()) for x in dL if dat_re.search(x)]
    if dat_list:
        dat_list = max(dat_list)
    print(dat_list)
    amount = dat_list


    # In[83]:


    amount = dat_list


    # In[84]:


    data = {'merchant_name':mer_name,'date':date,'amount':amount}


    # In[85]:

    ss_files = glob(f"../cashflow_backend/main/test_img/*")
    # print(f"ss_fls->{ss_files}")
    for f in ss_files:
        os.remove(f)
    return data


# In[ ]:





# In[ ]:




