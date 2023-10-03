import os
import re
import tkinter as tk
from tkinter import ttk, messagebox

# remove shortcut from user commands
def remove_shortcut(hotkey_to_remove):
    cmds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UserCommands.ahk")

    with open(cmds_path, 'r') as ahk_file:
        cmds = ahk_file.read()
    
    pattern = fr'\nelse if shortcut = {re.escape(hotkey_to_remove)}[^}}]*\n\s*\{{[^}}]*\n\s*}}'
    matches = re.findall(pattern, cmds)

    removed = False
    new_cmds = cmds

    for match in matches:
        if hotkey_to_remove in match:
            new_cmds = new_cmds.replace(match, '')
            removed = True

    if removed:
        with open(cmds_path, 'w') as ahk_file:
            ahk_file.write(new_cmds)

        messagebox.showinfo("Info", f"The shortcut '{hotkey_to_remove}' has been removed.")
    else:
        messagebox.showinfo("Info", f"No matching shortcut found for '{hotkey_to_remove}'.")

#theme
bg = '#1d1f21'
bg2 = '#282a2e'
fg = '#c5c8c6'
font= ('Segoe UI', 12)

# build widgets
root = tk.Tk()
root.title("Remove Shortcut")
root.configure(bg=bg)

style = ttk.Style()
style.theme_use("clam")

frame = tk.Frame(root, padx=6, pady=10, bg=bg)
frame.pack()

tk.Label(frame, text="Hotkey Phrase:", bg=bg, fg=fg, font=font, padx=6).pack(side=tk.LEFT)
hotkey = tk.Entry(frame, bg=bg2, foreground=fg, borderwidth=0, font=font)
hotkey.pack(side=tk.LEFT)

tk.Button(root, text="Remove Shortcut", command=lambda: remove_shortcut(hotkey.get()), bg=bg2, fg=fg, borderwidth=0, font=font).pack(padx=10, pady=10)

root.mainloop()
