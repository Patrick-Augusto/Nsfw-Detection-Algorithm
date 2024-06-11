import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
import time

# Number of threads to process the files
number_of_threads = 10

def process_file(file_name):
    start_time = time.time()
    elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(file_name)
    end_time = time.time()
    print(file_name, nsfw_probabilities)
    print("Processing time: ", end_time - start_time, "seconds")
    if max(nsfw_probabilities) > 1:
        print("The maximum NSFW probability is greater than 0.8")

def process_files():
    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        while True:
            file_name = file_queue.get()
            if file_name is None:
                break
            executor.submit(process_file, file_name)


nsfw_probability_threshold = 0.8
nsfw_probability = 0.0
working_directory = "C:\\Videos"
nsfw_directory = "C:\\Videos NSFW"
processed_files_list = []
file_queue = queue.Queue()
number_of_threads = 10



def check_directories():
    if not os.path.isdir(working_directory):
        print("Working directory does not exist:", working_directory)
        exit()

    if not os.path.isdir(nsfw_directory):
        print("NSFW directory does not exist:", nsfw_directory)
        exit()
        

def process_files():
    while True:
        start_time = time.time()  
        file_name = file_queue.get()
        if file_name is None:
            break

        elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(file_name)
        print(file_name, nsfw_probabilities)
        if max(nsfw_probabilities) > 1:
            print("The maximum NSFW probability is greater than 0.8")

        if any([nsfw_p > nsfw_probability_threshold for nsfw_p in nsfw_probabilities]):
            if file_name.endswith(".mp4") or file_name.endswith(".avi") or file_name.endswith(".mov"):
                shutil.move(file_name, os.path.join(nsfw_directory, os.path.basename(file_name)))
                print("The video is NSFW.")
            else:
                print("The image is not NSFW.")

        processed_files_list.append((file_name, elapsed_seconds))
        end_time = time.time()  
        elapsed_time = end_time - start_time  
        active_threads = threading.active_count()
        print(f"Processed {file_name} in {elapsed_time:.2f} seconds using {active_threads} threads.")



class MyHandler(FileSystemEventHandler):
   
    def on_created(self, event):
      
        if event.is_directory:
            return
        file_queue.put(event.src_path)
        

def start_observer():
   
    observer = Observer()
    observer.schedule(MyHandler(), working_directory, recursive=False)
    observer.start()
    return observer

def start_threads():
 
    threads = []
    for i in range(number_of_threads):
        thread = threading.Thread(target=process_files)
        threads.append(thread)
        thread.start()
    return threads  

def stop_threads(threads):
    
    for i in range(number_of_threads):
        file_queue.put(None)

   
    for thread in threads:
        thread.join()
        

def main():
  
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
