import opennsfw2 as n2
import os
import shutil
import time
import glob
import queue
import threading

threshold = 0.8
working_dir = "C:\\Images"
nsfw_dir = "C:\\Nsfw"
processed_files = []
file_queue = queue.Queue()

if not os.path.isdir(working_dir):
    print("Working directory does not exist:", working_dir)
    exit()

if not os.path.isdir(nsfw_dir):
    print("NSFW directory does not exist:", nsfw_dir)
    exit()

def process_files():
    while True:
        try:
            fname = file_queue.get_nowait()
        except queue.Empty:
            break
        
        nsfw_probability = n2.predict_image(fname)
        print(fname, nsfw_probability)
        if nsfw_probability > threshold:
            shutil.move(fname, os.path.join(nsfw_dir, os.path.basename(fname)))
        processed_files.append(fname)

while True:
    new_files = [f for f in glob.glob(os.path.join(working_dir, "*.jpg")) + glob.glob(os.path.join(working_dir, "*.png")) + glob.glob(os.path.join(working_dir, "*.webp"))+ glob.glob(os.path.join(working_dir, "*.jpeg")) if f not in processed_files]
    
    if new_files:
        for fname in new_files:
            file_queue.put(fname)
    
    while not file_queue.empty():
        threads = []
        for i in range(10):
            t = threading.Thread(target=process_files)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    
    time.sleep(1)