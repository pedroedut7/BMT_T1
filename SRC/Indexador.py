import re
import csv
import os
import nltk
import math
import pandas as pd
import numpy as np
import logging
import configparser
from lxml import etree
from collections import Counter
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

logging.info('Inicializando o indexador...')

diretorio = os.getcwd()
data = diretorio + "/data"
config = diretorio + "/CONFIG"
result = diretorio + "/RESULT"

# Processa arquivo das consultas e esperados
logging.info('Lendo o arquivo CONFIG')

cfig = configparser.ConfigParser()
cfig.read(config + '/INDEX.CFG')

leia = result + cfig.get('CONFIGS', 'LEIA')
escreva = result + cfig.get('CONFIGS', 'ESCREVA')

logging.info('Preparando os dados para o calculo da matriz tf-idf')

df_words = pd.read_csv(leia, delimiter = ';') 
counters = []
max_tf = {} # So preciso saber quantas vezes o termo mais frequente aparece, tfn = numero de aparicoes do meu termo/ numero de aparicoes do termo mais frequente
last_doc = 0

for lista in df_words.LIST:
    tf_counter = Counter(eval(lista))
    counters.append(tf_counter) # Vai me ajudar depois
    for record in tf_counter:
        try:
            if max_tf[record] < tf_counter[record]: max_tf[record] = tf_counter[record]
        except:
            max_tf[record] = tf_counter[record]
            
N = len(df_words.WORD)
M = max(max_tf.keys())
tf_idf_matrix = np.zeros((M, N)) # Cria matriz td-idf com M (Número de documentos) linhas e N (Número de palavras) colunas

# Tenho tudo pra calcular a matriz!

logging.info('Calculando a matriz')

words = df_words.WORD
word_list = df_words.LIST

idf_num = math.log(M) # Calculando o numerador do log

for i, word in enumerate(df_words.WORD):
    appearance_count_in_doc = counters[i]
    idf_denom = math.log(len(appearance_count_in_doc))
    idf = idf_num - idf_denom
    for doc_num in appearance_count_in_doc:
        tf = appearance_count_in_doc[doc_num]/max_tf[doc_num]
        tf_idf_matrix[doc_num-1][i] = tf * idf

logging.info('Escrevendo a matriz no csv') # Vou escrever o meu vetor das palavras na primeira linha e o resto vai levar minha matriz tf-idf

with open(escreva, 'w') as csvfile:
    
    fieldnames = ['LinhasMatriz']
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    
    writer.writerow({'LinhasMatriz': str(list(np.array(words)))})
    
    for linha in tf_idf_matrix:
        writer.writerow({'LinhasMatriz': str(list(linha))})
        
logging.info('Indexador finalizado')