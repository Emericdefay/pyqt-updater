import threading
import tkinter as tk
from tkinter import ttk
import time
import requests
import os
from tqdm import tqdm
import logging

from updater.paths import APP_PATH
from updater.settings import UPD_HEX_C
from updater.dialog import dialog_error

class DownloadProgressBar(tk.Frame):
    def __init__(self, parent, url):
        tk.Frame.__init__(self, parent, bg=UPD_HEX_C)
        self.url = url
        self.parent = parent
        self.message = "Update ..."
        self.message_label = tk.Label(self, text=self.message, bg=UPD_HEX_C)
        self.message_label.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=260, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack()

        self.bytes_label = tk.Label(self, text='',bg=UPD_HEX_C,)
        self.bytes_label.pack()

        self.speed_label = tk.Label(self, text='',bg=UPD_HEX_C,)
        self.speed_label.pack()

        self.start()

    def download(self):
        response = requests.get(self.url, stream=True)

        total_size = int(response.headers.get('Content-Length', 0))
        block_size = 1024

        bytes_read = 0
        try:
            with open(f"{APP_PATH}", "wb") as file:
                start_time = time.time()
                for chunk in tqdm(response.iter_content(block_size), total=total_size, unit='B', unit_scale=True, dynamic_ncols=True):
                    bytes_read += len(chunk)
                    progression = float(bytes_read) / float(total_size) * 100.0
                    elapsed_time = time.time() - start_time
                    speed_debit = bytes_read / 1024.0 / elapsed_time

                    self.bytes_label.config(text=f'{bytes_read / 1024.0:.2f} KB')
                    self.speed_label.config(text=f'{elapsed_time:.2f} s / {speed_debit:.2f} KB/s')
                    self.progress_var.set(progression)
                    file.write(chunk)
        except PermissionError as p:
            report = PermissionError("The application is still open, close it before update.")
            dialog_error(report)
            logging.error(f"Application still open : {p}", exc_info=True)
            os._exit(0)
        except Exception as e:
            logging.error(f"Errors in download : {e}", exc_info=True)


        self.close_thread()

    def start(self):
        threading.Thread(target=self.download).start()

    def close_thread(self):
        self.parent.destroy()
        self.parent.quit()
