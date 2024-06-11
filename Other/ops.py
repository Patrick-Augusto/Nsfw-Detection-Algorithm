import opennsfw2 as n2
import os
import shutil
import time
import glob
import queue
import threading

threshold = 0.8
working_dir = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Images"
nsfw_dir = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Nsfw"
processed_files = []
file_queue = queue.Queue()
num_threads = 10

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

threads = []
for i in range(num_threads):
    t = threading.Thread(target=process_files)
    threads.append(t)
    t.start()

while True:
    new_files = [f for f in glob.glob(os.path.join(working_dir, "*.[jJ][pP][eE]?[gG]")) + glob.glob(os.path.join(working_dir, "*.[pP][nN][gG]")) + glob.glob(os.path.join(working_dir, "*.[wW][eE][bB][pP]")) if f not in processed_files]
    
    if new_files:
        for fname in new_files:
            file_queue.put(fname)
    
    time.sleep(1)

for i in range(num_threads):
    file_queue.put(None)

for t in threads:
    t.join()