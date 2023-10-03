import os
import re
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from win32com.client import Dispatch

# search file explorer for a file path
def browse_file():
    selected_file = filedialog.askopenfilename()
    global path
    path.delete(0, tk.END)
    path.insert(0, selected_file)

# add to usercommands
def add_shortcut(hotkey, comment, runstring):
    # ahk template for the usercommands script
    template = f"""
else if shortcut = {hotkey} ; {comment}
{{
    gui_destroy()
    Run {runstring}
}}
    """

    # validation
    cmds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UserCommands.ahk")

    with open(cmds_path, 'r') as ahk_file:
        cmds = ahk_file.read()

    pattern = r'if shortcut = (\w+)\s*;'
    current_hotkeys = re.findall(pattern, cmds)

    found = False
    for i in current_hotkeys:
        if hotkey.startswith(i) or i.startswith(hotkey):
            found = True
            conflict = i
            break

    if found:
        messagebox.showinfo("Warning", f"The hotkey '{hotkey}' has a conflict with the existing hotkey '{conflict}'")
        return

    if os.path.exists(runstring) or (urlparse(runstring).scheme and urlparse(runstring).netloc):
        # add to user commands
        with open(cmds_path, 'a') as ahk_file:
            ahk_file.write(template)
        messagebox.showinfo("Success", "Hotkey added. Please reload the script.")
        root.destroy()
    else:
        messagebox.showinfo("Failed", "Your shortcut wasn't recognised as a url or filepath.")
    return

# theme
bg = '#1d1f21'
bg2 = '#282a2e'
fg = '#c5c8c6'
font= ('Segoe UI', 12)

# build widgets
root = tk.Tk()
root.title("Add File/App Shortcut")
root.configure(bg=bg)

style = ttk.Style()
style.theme_use("clam")

frame = tk.Frame(root, padx=6, bg=bg)
frame.pack()

frameleft = tk.Frame(frame, padx=6, bg=bg)
frameleft.pack(side=tk.LEFT)
tk.Label(frameleft, text="Hotkey Phrase:", bg=bg, fg=fg, font=font).pack()
hotkey = tk.Entry(frameleft, bg=bg2, foreground=fg, borderwidth=0, font=font)
hotkey.pack()

frameright = tk.Frame(frame, padx=6, bg=bg)
frameright.pack(side=tk.LEFT)
tk.Label(frameright, text="HotKey Comment:", bg=bg, fg=fg, font=font).pack()
comment = tk.Entry(frameright, bg=bg2, foreground=fg, borderwidth=0, font=font)
comment.pack()

tk.Label(root, text="Application Path (to exe) or File:", bg=bg, fg=fg, font=font).pack()

frame1 = tk.Frame(root, padx=6, bg=bg)
frame1.pack(pady=5)

path = tk.Entry(frame1, width=35, bg=bg2, foreground=fg, borderwidth=0, font=font)
path.pack(side=tk.LEFT)
tk.Button(frame1, text="Browse", command=browse_file, bg=bg2, fg=fg, borderwidth=0, font=font).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Add Shortcut", command=lambda: add_shortcut(hotkey.get(), comment.get(), path.get()), bg=bg2, fg=fg, borderwidth=0, font=font).pack(padx=10, pady=10)

root.mainloop()
