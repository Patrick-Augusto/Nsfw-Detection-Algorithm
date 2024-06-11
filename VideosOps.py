import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

number_of_threads = 10
nsfw_probability_threshold = 0.8
working_directory = "C:\\Videos"
nsfw_directory = "C:\\Videos NSFW"
file_queue = queue.Queue()

def process_file(file_name):
    start_time = time.time()
    elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(file_name)
    end_time = time.time()
    print(file_name, nsfw_probabilities)
    print("Processing time: ", end_time - start_time, "seconds")
    
    if max(nsfw_probabilities) > 1:
        print("The maximum NSFW probability is greater than 0.8")

    if any([nsfw_p > nsfw_probability_threshold for nsfw_p in nsfw_probabilities]):
        if file_name.endswith((".mp4", ".avi", ".mov")):
            shutil.move(file_name, os.path.join(nsfw_directory, os.path.basename(file_name)))
            print("The video is NSFW.")
        else:
            print("The image is not NSFW.")

def process_files():
    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        while True:
            file_name = file_queue.get()
            if file_name is None:
                break
            future = executor.submit(process_file, file_name)
            print("Number of active threads: ", len(executor._threads))

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

def start_processing():
    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        while True:
            file_name = file_queue.get()
            if file_name is None:
                break
            executor.submit(process_file, file_name)

def main():
    if not os.path.isdir(working_directory):
        print("Working directory does not exist:", working_directory)
        return

    if not os.path.isdir(nsfw_directory):
        print("NSFW directory does not exist:", nsfw_directory)
        return

    observer = start_observer()

    processing_thread = threading.Thread(target=start_processing)
    processing_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    file_queue.put(None)
    processing_thread.join()
    observer.join()

if __name__ == "__main__":
    main()
