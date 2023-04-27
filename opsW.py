import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

threshold = 0.8
working_dir = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Images"
nsfw_dir = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Nsfw"
processed_files = []
file_queue = queue.Queue()
num_threads = 2

if not os.path.isdir(working_dir):
    print("Working directory does not exist:", working_dir)
    exit()

if not os.path.isdir(nsfw_dir):
    print("NSFW directory does not exist:", nsfw_dir)
    exit()

def process_files():
    while True:
        fname = file_queue.get()
        if fname is None:
            break
        
        nsfw_probability = n2.predict_image(fname)
        print(fname, nsfw_probability)
        if nsfw_probability > threshold:
            shutil.move(fname, os.path.join(nsfw_dir, os.path.basename(fname)))
        processed_files.append(fname)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_queue.put(event.src_path)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, working_dir, recursive=False)
observer.start()

threads = []
for i in range(num_threads):
    t = threading.Thread(target=process_files)
    threads.append(t)
    t.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

for i in range(num_threads):
    file_queue.put(None)

for t in threads:
    t.join()

observer.join()