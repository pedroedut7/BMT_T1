import re
import os
import csv
import logging
import configparser
from lxml import etree
from utility import calculaNota

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

logging.info('Inicializando o processador...')

diretorio = os.getcwd()
data = diretorio + "/data"
config = diretorio + "/CONFIG"
result = diretorio + "/RESULT"

# Processa arquivo das consultas e esperados
logging.info('Lendo o arquivo CONFIG')

cfig = configparser.ConfigParser()
cfig.read(config + '/PC.CFG')

leia = data + cfig.get('CONFIGS', 'LEIA')
consultas = result + cfig.get('CONFIGS', 'CONSULTAS')
esperados = result + cfig.get('CONFIGS', 'ESPERADOS')

parser = etree.XMLParser()
tree = etree.parse(leia, parser)
root = tree.getroot()

logging.info('Criando o csv com as consultas')

with open(consultas, 'w') as csvfile:
    
    fieldnames = ['QueryNumber', 'QueryText']
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    
    for query in root.findall('QUERY'):
        QueryNumber = query.find('QueryNumber').text
        QueryText = re.sub(r'\s+', ' ', query.find('QueryText').text.replace('\n', '').strip()).upper() # Desculpe por isso!
        
        # Escreve os dados no arquivo CSV
        writer.writerow({'QueryNumber': QueryNumber, 'QueryText': QueryText})

logging.info('Criando o csv com os resultados esperados')

with open(esperados, 'w') as csvfile:
    
    fieldnames = ['QueryNumber', 'DocNumber', 'DocVotes']
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';')
    writer.writeheader()
    
    for query in root.findall('QUERY'):
        QueryNumber = query.find('QueryNumber').text
        Records = query.find('Records')
        
        for item in Records.findall('Item'):
            DocNumber = item.text
            Score = calculaNota(item.attrib.get('score'))
            
            writer.writerow({'QueryNumber': QueryNumber, 'DocNumber': DocNumber, 'DocVotes': Score})

logging.info('Processador finalizado!')