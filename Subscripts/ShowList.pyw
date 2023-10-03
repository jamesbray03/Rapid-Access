import os
import re
import tkinter as tk
from tkinter import ttk

cmds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UserCommands.ahk")

with open(cmds_path, 'r') as ahk_file:
    cmds = ahk_file.read()

# format strings from user commands
pattern = r'if shortcut = ([^;]+)\s*;'
hotkeys = re.findall(pattern, cmds)
hotkeys = [hotkey.replace('%A_Space%', '_') for hotkey in hotkeys]

pattern = r'if shortcut = [^;]+ ; (.+)'
comments = re.findall(pattern, cmds)

# build widgets
bg = '#1d1f21'
bg2 = '#282a2e'
fg = '#c5c8c6'
font = ('Segoe UI', 12)

root = tk.Tk()
root.title("Hotkey List")
root.configure(bg=bg)

style = ttk.Style()
style.theme_use("clam")

frame = tk.Frame(root, bg=bg)
frame.pack(fill="both", expand=True)

style.configure("Custom.Vertical.TScrollbar", troughcolor=bg, borderwidth=0, highlightthickness=0, gripcount=0,
                background=bg2, darkcolor=bg2, lightcolor=bg2, arrowcolor=fg)

scrollbar = ttk.Scrollbar(frame, orient="vertical", style="Custom.Vertical.TScrollbar")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(frame, columns=("Column 1", "Column 2"), show="headings", yscrollcommand=scrollbar.set, style="Custom.Treeview")
tree.heading("Column 1", text="Hotkey", anchor=tk.W)
tree.heading("Column 2", text="Action", anchor=tk.W)
tree.pack(expand=True)

scrollbar.config(command=tree.yview)

style.configure("Custom.Treeview.Heading", font=font, foreground=fg, background=bg2, borderwidth=0, hovercolor=bg2)
style.configure("Custom.Treeview", font=font, foreground=fg, background=bg, borderwidth=0)

style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])

for i in range(len(hotkeys)):
    tree.insert("", "end", values=(hotkeys[i], comments[i]))

root.mainloop()
