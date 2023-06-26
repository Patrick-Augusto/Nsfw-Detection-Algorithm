import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define o limiar de probabilidade para mover uma imagem para o diretório NSFW
nsfw_probability_threshold = 0.8

# Define os diretórios de trabalho e NSFW
working_directory = "C:\\Images"
nsfw_directory = "C:\\Nsfw"

# Lista para armazenar os arquivos processados.
processed_files_list = []

# Fila para armazenar os arquivos a serem processados.
file_queue = queue.Queue()

# Número de threads para processar os arquivos.
number_of_threads = 10

def check_directories():
    # Verifica se os diretórios especificados existem
    if not os.path.isdir(working_directory):
        print("Working directory does not exist:", working_directory)
        exit()

    if not os.path.isdir(nsfw_directory):
        print("NSFW directory does not exist:", nsfw_directory)
        exit()
#How do I make my function def process_files , if checked twice? 

def process_files():
    # Processa os arquivos na fila
    while True:
        file_name = file_queue.get()
        if file_name is None:
            break
         
        # Usa a biblioteca opennsfw2 para prever a probabilidade de uma imagem ser NSFW
        nsfw_probability = n2.predict_image(file_name)
        print(file_name, nsfw_probability)
        
        # Move a imagem para o diretório NSFW se a probabilidade for maior que o limiar definido
        if nsfw_probability > nsfw_probability_threshold:
            shutil.move(file_name, os.path.join(nsfw_directory, os.path.basename(file_name)))
            print("The video is NSFW.")
        else:                                      
           print("The image is not NSFW.")

        # Adiciona o arquivo à lista de arquivos processados
        processed_files_list.append(file_name)

class MyHandler(FileSystemEventHandler):
    # Classe para lidar com eventos do sistema de arquivos
    def on_created(self, event):
        # Adiciona o arquivo à fila quando um novo arquivo é criado no diretório observado
        if event.is_directory:
            return
        file_queue.put(event.src_path)

def start_observer():
    # Inicia o observador do sistema de arquivos para observar o diretório especificado
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, working_directory, recursive=False)
    observer.start()
    return observer

def start_threads():
    # Inicia as threads para processar os arquivos na fila
    threads = []
    for i in range(number_of_threads):
        thread = threading.Thread(target=process_files)
        threads.append(thread)
        thread.start()
    return threads

def stop_threads(threads):
    # Para as threads adicionando None à fila para cada thread
    for i in range(number_of_threads):
        file_queue.put(None)

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()
        

def main():
    # Função principal para executar o programa
    check_directories()
    observer = start_observer()
    threads = start_threads()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    stop_threads(threads)
    observer.join()

if __name__ == "__main__":
    main()
