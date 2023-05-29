import openai
import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define a chave da API OpenAI e o modelo a ser utilizado
openai.api_key = "sua_chave_API_do_OpenAI"
model_engine = "davinci"  # Pode ser substituído por outro modelo OpenAI

# Define o limiar de probabilidade para mover uma imagem para o diretório NSFW
nsfw_probability_threshold = 0.8

# Define os diretórios de trabalho e NSFW
working_directory = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Images"
nsfw_directory = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Nsfw"

# Lista para armazenar os arquivos processados
processed_files_list = []

# Fila para armazenar os arquivos a serem processados
file_queue = queue.Queue()

# Número de threads para processar os arquivos
number_of_threads = 10


def check_directories():
    # Verifica se os diretórios especificados existem
    if not os.path.isdir(working_directory):
        print("Working directory does not exist:", working_directory)
        exit()

    if not os.path.isdir(nsfw_directory):
        print("NSFW directory does not exist:", nsfw_directory)
        exit()


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

        # Adiciona o arquivo à lista de arquivos processados
        processed_files_list.append(file_name)

        # Usa o modelo OpenAI para gerar uma descrição para a imagem
        try:
            with open(file_name, "rb") as image_file:
                image_data = image_file.read()
                response = openai.Completion.create(engine=model_engine, prompt=f"Describe the image in one sentence:\n{image_data.decode('ISO-8859-1')}\n", max_tokens=50)
                image_description = response.choices[0].text.strip()
                print(image_description)
        except Exception as e:
            print(e)


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
  
# Inicia, gerencia e aguarda as threads de processamento de arquivos
threads = []
for i in range(number_of_threads):
thread = threading.Thread(target=process_files)
thread.start()
threads.append(thread)
for thread in threads:
    thread.join()
    if name == "main":
# Verifica se os diretórios existem
check_directories()

# Inicia o observador do sistema de arquivos
observer = start_observer()

try:
    # Inicia as threads de processamento de arquivos
    start_threads()
except KeyboardInterrupt:
    # Interrompe o programa se o usuário pressionar CTRL-C
    pass

# Para o observador do sistema de arquivos
observer.stop()
observer.join()

# Imprime a lista de arquivos processados
print("Processed files:")
for file_name in processed_files_list:
    print(file_name)

