import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import threading

# Function to load the words from a selected file
def load_words():
    file_path = filedialog.askopenfilename(title="Select Word List File", filetypes=(("Text Files", "*.txt"),))
    if file_path:
        with open(file_path, 'r') as file:
            global words
            words = [line.strip() for line in file]
        messagebox.showinfo("Success", "Words loaded successfully!")

# Function to start the search process
def start_search():
    if not words:
        messagebox.showwarning("Warning", "Please load a word list first!")
        return

    # Disable buttons during the search process
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    def search():
        try:
            # Initialize the Edge WebDriver
            driver = webdriver.Edge()

            for i in range(38):  
                if not running:
                    break
                word = random.choice(words)
                driver.get("https://www.bing.com/")
                search_box = driver.find_element(By.NAME, "q")
                search_box.send_keys(word)
                search_box.submit()
                print(i)
                time.sleep(35)
        finally:
            driver.quit()
            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)

    global running
    running = True
    threading.Thread(target=search).start()

# Function to stop the search process
def stop_search():
    global running
    running = False
    messagebox.showinfo("Stopped", "Search process has been stopped.")

# Initialize GUI window
root = tk.Tk()
root.title("Automated Web Search")

# Initialize global variables
words = []
running = False

# Create and place GUI widgets
load_button = tk.Button(root, text="Load Word List", command=load_words)
load_button.pack(pady=10)

start_button = tk.Button(root, text="Start Search", command=start_search)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Search", command=stop_search, state=tk.DISABLED)
stop_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
