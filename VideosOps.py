import opennsfw2 as n2
import os
import shutil
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the probability threshold for moving an image or video into the NSFW directory
nsfw_probability_threshold = 0.8
nsfw_probability = 0.0
# Set the working and NSFW directories
working_directory = "C:\\Videos"
nsfw_directory = "C:\\Videos NSFW"

# List to store the processed files
processed_files_list = []

# Queue to store the files to be processed
file_queue = queue.Queue()

# Number of threads to process the files
number_of_threads = 10


# List to store the processed files
def check_directories():
    # Checks if the specified directories exist
    if not os.path.isdir(working_directory):
        print("Working directory does not exist:", working_directory)
        exit()

    if not os.path.isdir(nsfw_directory):
        print("NSFW directory does not exist:", nsfw_directory)
        exit()
        
def process_files():
    while True:
        file_name = file_queue.get()
        if file_name is None:
            break

        elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(file_name)
        print(file_name, nsfw_probabilities)
        if max(nsfw_probabilities) > 1:
            print("The maximum NSFW probability is greater than 0.8")

        # Move image or video to NSFW directory if probability is greater than defined threshold
        if any([nsfw_p > nsfw_probability_threshold for nsfw_p in nsfw_probabilities]):
            if file_name.endswith(".mp4") or file_name.endswith(".avi") or file_name.endswith(".mov"):
                shutil.move(file_name, os.path.join(nsfw_directory, os.path.basename(file_name)))
                print("The video is NSFW.")
            else:
                print("The image is not NSFW.")

        processed_files_list.append((file_name, elapsed_seconds))  # Store file and elapsed time

end_time = time.time()  # End measuring time



class MyHandler(FileSystemEventHandler):
    # Class to handle file system events
    def on_created(self, event):
        # Adds the file to the queue when a new file is created in the observed directory
        if event.is_directory:
            return
        file_queue.put(event.src_path)
        

def start_observer():
    # Starts the file system observer to observe the specified directory
    observer = Observer()
    observer.schedule(MyHandler(), working_directory, recursive=False)
    observer.start()
    return observer

def start_threads():
    # Starts the threads to process the files in the queue
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
