from lxml import etree
from collections import Counter
import re
import csv
import os
import nltk
import math
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def calculaNota(notas):
    nota_final = 0
    for nota in notas:
        nota_final += int(nota)
    
    return nota_final

def getAbstracts(root):
    abstracts = {}
    for record in root.findall('RECORD'):
        RECORDNUM = int(record.find('RECORDNUM').text)
        try:
            try:
                ABSTRACT = re.sub(r'\s+', ' ', record.find('ABSTRACT').text.replace('\n', '').strip()).upper() # Desculpe por isso!
            except:
                ABSTRACT = re.sub(r'\s+', ' ', record.find('EXTRACT').text.replace('\n', '').strip()).upper()

            abstracts[RECORDNUM] = ABSTRACT

        except:
            abstracts[RECORDNUM] = ""
            continue
    
    return abstracts

def process(abstracts):
    word_count = {}
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    for doc in abstracts:
        word_list = word_tokenize(abstracts[doc])
        word_filtered = [stemmer.stem(word).upper() for word in word_list if len(word) > 2 and re.match(r'^[A-Z]+$', word) and (word.lower() not in stop_words)] # Preparando para o indexador

        for word in word_filtered:
            try:
                word_list = word_count[word] 
                word_list.append(doc)
            except:
                word_count[word] = [doc]
    
    return word_count

def getAbstractsLength(root):
    abstracts = getAbstracts(root)
    docLength = {}
    
    for doc in abstracts:
        word_list = word_tokenize(abstracts[doc])
        word_filtered = [word for word in word_list if len(word) > 2 and re.match(r'^[A-Z]+$', word)]
        
        docLength[doc] = len(word_filtered)
    
    return docLength

def write(dictionary, path):
    with open(path, 'w') as csvfile:

        fieldnames = ['WORD', 'LIST']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
        writer.writeheader()

        for word in dictionary:
            writer.writerow({'WORD': word, 'LIST': dictionary[word]})