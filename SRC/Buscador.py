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
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

logging.info('Inicializando o buscador...')

diretorio = os.getcwd()
data = diretorio + "/data"
config = diretorio + "/CONFIG"
result = diretorio + "/RESULT"

# Processa arquivo das consultas e esperados
logging.info('Lendo o arquivo CONFIG')

cfig = configparser.ConfigParser()
cfig.read(config + '/BUSCA.CFG')

modelo = result + cfig.get('CONFIGS', 'MODELO')
consultas = result + cfig.get('CONFIGS', 'CONSULTAS')
resultados = result + cfig.get('CONFIGS', 'RESULTADOS')

# Processa as consultas transformando-as em vetor e pega a matriz do csv (demora muito!)
logging.info('Lendo o arquivo CONSULTAS e MODELO')

df_consultas = pd.read_csv(consultas, delimiter=';')
df_modelo = pd.read_csv(modelo, delimiter=';')

vetor_original = eval(df_modelo.LinhasMatriz.loc[0])
matriz = np.array(np.array([eval(df_modelo.LinhasMatriz.iloc[i]) for i in range(1, len(df_modelo.LinhasMatriz))]))

map_word_to_index = {}
for i, word in enumerate(vetor_original):
    map_word_to_index[word] = i
    
queries_list = {}
stemmer = PorterStemmer()
for i in range(len(df_consultas.QueryNumber)):
    query = df_consultas.QueryText.iloc[i]
    query_token = word_tokenize(query)
    word_filtered = [stemmer.stem(word).upper() for word in query_token if len(word) > 2 and re.match(r'^[A-Z]+$', word)] 
    queries_list[df_consultas.QueryNumber.iloc[i]] = word_filtered
    
logging.info('Transformando as consultas em vetor')

queries_vector = {}
vec_size = len(vetor_original)
for query in queries_list:
    query_list = queries_list[query]
    query_vector = np.zeros(vec_size)
    for word in query_list:
        try:
            i = map_word_to_index[word]
            query_vector[i] += 1
        except:
            continue
            
    queries_vector[query] = query_vector
    
# Classificando as consultas
logging.info('Classificando as consultas')

queries_classified = {i: matriz.dot(queries_vector[i]) for i in queries_vector}
relevance_query = {}

for query in queries_classified:
    resultado = queries_classified[query]
    index_doc = [(pontos, i+1) for i, pontos in enumerate(resultado)] # Me ajuda a ordenar os documentos mais relevantes
    index_doc.sort(reverse=True)
    relevance_query[query] = index_doc
    
logging.info('Calculando a distancia da query pro doc e preparando os resultados')
# Vou calcular a distancia com a matriz tf-idf, ja que ela contem a proporcao entre as palavras presentes em um documento e no final vai ser tudo normalizado

resultado_final = []

for query in relevance_query:
    relevance_list = relevance_query[query]
    for i, (pontos, doc) in enumerate(relevance_list): # Saiu feio, mas vai servir
        distance = np.linalg.norm(np.linalg.norm(matriz[doc-1]) - np.linalg.norm(queries_vector[query])) # Normalizando os vetores antes de achar as distancias
        resultado_final.append([query, i + 1, doc, distance])
        
logging.info('Preparando o CSV')

with open(resultados, 'w') as csvfile:
    
    fieldnames = ['QueryNumber', 'TermosOrdenados']
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    
    for linha in resultado_final:
        writer.writerow({'QueryNumber': linha[0], 'TermosOrdenados': linha[1:]})
        
logging.info('Acabou!')