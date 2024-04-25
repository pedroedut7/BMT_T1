import subprocess
import logging
import time

inicio = time.time()

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


path_processador = './SRC/Processador.py'
path_gerador_lista_invertida = './SRC/GeradorListaInvertida.py'
path_indexador = './SRC/Indexador.py'
path_buscador = './SRC/Buscador.py'

arquivos = [path_processador, path_gerador_lista_invertida, path_indexador, path_buscador]

for arquivo in arquivos:
    logging.info("Executando o arquivo: %s", arquivo)
    
    resultado = subprocess.run(["python", arquivo], text=True, stdout=subprocess.PIPE)
    
    if resultado.returncode != 0:
        logging.error("Erro ao executar o arquivo %s: %s", arquivo, resultado.stderr)
    else:
        logging.info("Arquivo %s executado com sucesso!", arquivo)
    
    if resultado.stdout:
        logging.info("Saída do arquivo %s: %s", arquivo, resultado.stdout)
        
print(f'O tempo total de execucao foi de {time.time() - inicio} segundos')