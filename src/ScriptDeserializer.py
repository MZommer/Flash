from Flash import Script
import json
import tkinter as tk
from tkinter import filedialog

DIALOG_FILETYPES = ("Binary files", "*.bin"), ("all files", "*.*")

root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', '1')

path = filedialog.askopenfilename(title="Select the Script file", filetypes=DIALOG_FILETYPES)
script = Script.Deserialize(path)
MapName = input("Write the song MapName: ") or "Dance"
song = script.makeBlueStar(MapName)

output = filedialog.asksaveasfilename(title="Save the Song file", initialfile=f"{MapName}.json", filetypes=[("JSON File", "*.json")])
with open(output, "w", encoding="utf-8") as f:
    json.dump(song, f)
print("Song saved successfully!")

