import logging
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
working_directory = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Videos"
nsfw_directory = "C:\\Users\\patri\\OneDrive\\Área de Trabalho\\Teste do algoritimo\\Videos NSFW"

# List to store the processed files
processed_files_list = []

# Queue to store the files to be processed
file_queue = queue.Queue()

# Number of threads to process the files
number_of_threads = 10

# Configure logging
logging.basicConfig(level=logging.INFO, filename='logfile.log', filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')

def check_directories():
    # Checks if the specified directories exist
    if not os.path.isdir(working_directory):
        logging.error("Working directory does not exist: %s", working_directory)
        exit()

    if not os.path.isdir(nsfw_directory):
        logging.error("NSFW directory does not exist: %s", nsfw_directory)
        exit()

# ...

def process_file(file_name):
    elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(file_name)
    logging.info("Processed file: %s, NSFW probabilities: %s", file_name, nsfw_probabilities)
    if max(nsfw_probabilities) > 1:
        logging.warning("The maximum NSFW probability is greater than 0.5")

    # Move image or video to NSFW directory if probability is greater than defined threshold
    if any(nsfw_p > nsfw_probability_threshold for nsfw_p in nsfw_probabilities):
        if file_name.endswith(".mp4") or file_name.endswith(".avi") or file_name.endswith(".mov"):
            shutil.move(file_name, os.path.join(nsfw_directory, os.path.basename(file_name)))
            logging.info("The video is NSFW: %s", file_name)
        else:
            logging.info("The image is not NSFW: %s", file_name)

    processed_files_list.append(file_name)

def process_files():
    while True:
        file_name = None  # Initialize with a default value
        try:
            file_name = file_queue.get(timeout=1)
            if file_name is None:
                break

            process_file(file_name)
        except queue.Empty:
            pass
        except Exception as e:
            logging.error("An error occurred while processing file: %s", file_name, exc_info=True)
            file_name = None  # Initialize file_name with a default value

# ...



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
    # Stops the threads by adding None to the queue for each thread
    for i in range(number_of_threads):
        file_queue.put(None)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def main():
    # Main function to run the program
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
