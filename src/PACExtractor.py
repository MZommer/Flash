from PAC import Pack
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', '1')
path = filedialog.askopenfilename(title="Select the Pack file", filetypes=(("Pack files", "*.pac"), ("all files", "*.*")))
if path == "":
    exit("Please select a PAC file.")
output = filedialog.askdirectory(title="Select The output folder")

with Pack(path) as pac:
    pac.extractall(output)
