from Flash import LyricScript, LyricData
import json
import tkinter as tk
from tkinter import filedialog

DIALOG_FILETYPES = ("Binary files", "*.bin"), ("all files", "*.*")

root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', '1')

DataPath = filedialog.askopenfilename(title="Select the LyricData file", filetypes=DIALOG_FILETYPES)
ans = input("Is the LyricData with one localization? (y/n) ")
legacy = ans.lower() == "y"
data = LyricData.Deserialize(DataPath, legacy=legacy)
print("Lyric Data parsed succesfully!")

ScriptPath = filedialog.askopenfilename(title="Select the LyricScript file", filetypes=DIALOG_FILETYPES)
script = LyricScript.Deserialize(ScriptPath)
print("Lyric Script parsed succesfully!")
clips = script.makeBlueStar(data)

output = filedialog.asksaveasfilename(title="Save the Lyrics clips", filetypes=[("JSON File", "*.json")])
with open(output, "w", encoding="utf-8") as f:
    json.dump(clips, f)
print("Clips saved successfully!")
