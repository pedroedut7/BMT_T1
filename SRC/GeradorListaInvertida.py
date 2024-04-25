import re
import csv
import os
import nltk
import logging
import configparser
from lxml import etree
from utility import getAbstracts, process, write
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

logging.info('Inicializando o gerador de lista invertida...')

diretorio = os.getcwd()
data = diretorio + "/data"
config = diretorio + "/CONFIG"
result = diretorio + "/RESULT"

# Processa arquivo das consultas e esperados
logging.info('Lendo o arquivo CONFIG')

cfig = configparser.ConfigParser()
cfig.read(config + '/CLI.CFG')

leia = cfig.get('CONFIGS', 'LEIA').replace(';', '", "')
leia = eval(f'["{leia}"]')
leia = [data + no_space.replace(" ", "")  for no_space in leia] # Tirando os espacos vazios de cada endereco e juntando tudo
escreva = result + cfig.get('CONFIGS', 'ESCREVA')

# Processando cada arquivo de consulta
logging.info('Juntando os arquivos de consulta')

abstracts = {}
for arquivo in leia:
    parser = etree.XMLParser()
    tree = etree.parse(arquivo, parser)
    root = tree.getroot()
    
    abstracts.update(getAbstracts(root))

# Processando cada arquivo de consulta
logging.info('Criando o dict com o mapeamento palavras -> documento')  
word_list = process(abstracts)

logging.info('Escrevendo no csv') 
write(word_list, escreva)

logging.info('Gerador de lista finalizado!')