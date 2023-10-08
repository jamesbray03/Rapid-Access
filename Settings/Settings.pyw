import os, re, psutil, subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from urllib.parse import urlparse
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

## FILES

main_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
builtin_path = os.path.join(main_dir, "Hotkeys", "BuiltinHotkeys.ahk")
custom_path = os.path.join(main_dir, "Hotkeys", "CustomHotkeys.ahk")
uninstall_path = os.path.join(main_dir, "unins000.exe")
ahk_path = os.path.join(main_dir, "AutoHotkey.exe")
main_path = os.path.join(main_dir, "Rapid-Access.ahk")

## FUNCTIONS

# breakdown the ahk hotkey scripts to their hotkeys
def get_script_hotkeys(script_path):
    with open(script_path, 'r') as ahk_file:
        script_contents = ahk_file.read()

    pattern = r'if shortcut = ([^;]+)\s*; (.+)'
    matches = re.findall(pattern, script_contents)

    hotkeys = []
    for match in matches:
        hotkey, comment = match
        hotkeys.append({'hotkey': hotkey, 'comment': comment})

    return hotkeys

# removes hotkey, app needs to be reloaded to save
def remove_hotkey(cmd_tree):
    selected_items = cmd_tree.selection()

    for item in selected_items:
        hotkey_to_remove = cmd_tree.item(item, "values")[0]

        with open(custom_path, 'r') as ahk_file:
            script_content = ahk_file.read()

        pattern = fr'else if shortcut = {re.escape(hotkey_to_remove)}[^}}]*\n\s*\{{[^}}]*\n\s*}}'
        matches = re.findall(pattern, script_content)

        removed = False
        for match in matches:
            if hotkey_to_remove in match:
                script_content = script_content.replace(match, '')
                removed = True

        if removed:
            with open(custom_path, 'w') as ahk_file:
                ahk_file.write(script_content)
            messagebox.showinfo("Info", f"The shortcut '{hotkey_to_remove}' has been removed.\n\nPlease reload the application with 'rel' to save your changes")
            update_table()
        else:
            messagebox.showinfo("Info", f"No matching shortcut found for '{hotkey_to_remove}'.")

# adds hotkey, app needs to be reloaded to save
def add_hotkey(hotkey, comment, link):
    if hotkey == '':
        messagebox.showinfo("Warning", f"Please assign a valid hotkey")
        return
    if comment == '':
        messagebox.showinfo("Warning", f"Please enter a comment")
        return
    if link == '':
        messagebox.showinfo("Warning", f"Please use a valid link")
        return

    # ahk template for the usercommands script
    template = f"""
else if shortcut = {hotkey} ; {comment}
{{
    gui_destroy()
    Run {link}
}}"""

    with open(custom_path, 'r') as ahk_file:
        cmds = ahk_file.read()

    with open(builtin_path, 'r') as ahk_file:
        cmds += ahk_file.read()

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

    if os.path.exists(link) or (urlparse(link).scheme and urlparse(link).netloc):
        # add to user commands
        with open(custom_path, 'a') as ahk_file:
            ahk_file.write(template)
        messagebox.showinfo("Success", f"Hotkey {hotkey} added.\n\nPlease reload the application with 'rel' to save your changes")
        update_table()
    else:
        messagebox.showinfo("Failed", f"{link} wasn't recognised as a url or filepath.")
    return

# terminates app
def terminate():
    terminated = False
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].startswith('AutoHotkey'):
            pid = process.info['pid']
            psutil.Process(pid).terminate()
            terminated = True

    if terminated:
        root.after(1, root.quit())
        messagebox.showinfo('Success', 'Rapid Access is no longer running.\n\nSettings will now close.')
    else:
        messagebox.showinfo('Failed', 'Unable to find current process')

# uninstalls app
def uninstall():
    proceeding = messagebox.askyesno('Proceed?', 'Are you sure you want to uninstall Rapid Access?')
    if proceeding:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].startswith('AutoHotkey'):
                pid = process.info['pid']
                psutil.Process(pid).terminate()

        root.after(1, subprocess.run(uninstall_path, shell=True, check=True))
        root.quit()

# search file explorer for a file path
def browse_file(output):
    selected_file = filedialog.askopenfilename()
    output.delete(0, tk.END)
    output.insert(0, selected_file)

# updates the custom hotkeys
def update_table():
    items = custom_tree.get_children()
    for item in items:
        custom_tree.delete(item)

    for i in get_script_hotkeys(custom_path):
        custom_tree.insert("", "end", values=(i['hotkey'], i['comment']))


## TKINTER APP
# use of if true statements is for development purposes 
if True:
    w, h = 510, 470

    root = tk.Tk()
    root.title("Rapid Access - Settings")
    root.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'Icons', 'RA.ico'))
    root.minsize(width=w, height=h)
    root.maxsize(width=w, height=h)

    # tkiner style config
    if True:
        style = ttk.Style()
        style.theme_use('default')

        dark_bg = '#1D1D21'
        light_bg = '#2C2F33'
        dark_text = '#989596'
        light_text = '#D2D4D3'
        highlight = '#4b6884'

        root.configure(bg=dark_bg)

        font = ('Segoe UI', 10)

        style.configure('Custom.TNotebook',
                            background=dark_bg,
                            tabposition='nw',
                            font=font,
                            borderwidth=0,
                            padx=5,
                            relief='flat')

        style.configure('Custom.TNotebook.Tab',
                            background=dark_bg,
                            foreground=light_text,
                            bordercolor=light_bg,
                            borderwidth=0,
                            relief='flat',
                            padding=[8, 5],
                            font=font)
        style.map("Custom.TNotebook.Tab", background=[("selected", light_bg)])

        style.configure("Custom.TLabel",
                    background=light_bg,
                    foreground=light_text,
                    font=font,
                    relief="flat",
                    borderwidth=0,
                    padding=(5, 5))

        style.configure('Custom.TFrame',
                background=light_bg,
                borderwidth=0,
                relief='flat')
        
        style.configure('Custom.TButton',
                background=light_bg,
                foreground=light_text,
                borderwidth=3,
                highlightcolor='#ff0000',
                font=font,
                relief='raised',
                padding=(5, 0))
        style.map('Custom.TButton', background=[('active', highlight)])

        style.configure('Custom.TEntry',
                foreground=dark_text,
                font=font,
                insertbackground=dark_text,
                relief='flat',
                borderwidth=0,
                padding=(5, 5))
        style.map('Custom.TEntry', fieldbackground=[('active', dark_bg), ('!active', dark_bg)])

        style.configure('Custom.Treeview',
                background=dark_bg,
                fieldbackground=dark_bg,
                foreground=dark_text,
                justify='center',
                font=font,
                rowheight=25,
                borderwidth=0,
                relief='flat',
                headingfont=font)

        style.configure('Custom.Treeview.Heading',
                background=light_bg,
                foreground=light_text,
                relief='flat',
                font=font) 
        style.map('Custom.Treeview.Heading', background=[("active", light_bg)])

    # tkinter widgets
    tabs = ttk.Notebook(root, style='Custom.TNotebook')
    if True:
        if True: # current hotkeys tab
            tab = ttk.Frame(tabs, style='Custom.TFrame', padding=5)
            tabs.add(tab, text="Current Hotkeys")

            if True: # built-in help label
                ttk.Label(tab, style="Custom.TLabel", text=f"Built-In Commands:").pack()
            
            if True: # built-in hotkeys table
                treeframe = ttk.Frame(tab)
                treeframe.pack(fill='both', padx=12)

                tree = ttk.Treeview(treeframe, style='Custom.Treeview', columns=("Column 1", "Column 2"), selectmode="none", height=4, show="headings")
                tree.heading("Column 1", text="Hotkey", anchor=tk.N)
                tree.heading("Column 2", text="Comment", anchor=tk.N)
                tree.pack(expand=True, fill='both')

                for i in get_script_hotkeys(builtin_path):
                    tree.insert("", "end", values=(i['hotkey'], i['comment']))
            
            if True: # custom help label
                ttk.Label(tab, style="Custom.TLabel", text="Custom Commands:").pack()

            if True: # custom hotkeys table
                treeframe = ttk.Frame(tab)
                treeframe.pack(fill='both', padx=12)

                scrollbar = ttk.Scrollbar(treeframe, orient="vertical", style="Custom.Vertical.TScrollbar")
                # scrollbar.pack(side="right", fill="y")

                custom_tree = ttk.Treeview(treeframe, style='Custom.Treeview', columns=("Column 1", "Column 2"), show="headings", height=6, yscrollcommand=scrollbar.set)
                custom_tree.heading("Column 1", text="Hotkey", anchor=tk.N)
                custom_tree.heading("Column 2", text="Comment", anchor=tk.N)

                custom_tree.pack(expand=True, fill='both')

                scrollbar.config(command=custom_tree.yview)

                update_table()

            if True: # remove button
                remove_button = ttk.Button(tab, style='Custom.TButton', text='Remove Hotkey', command=lambda: remove_hotkey(custom_tree))
                remove_button.pack(fill='x', padx=12)

        if True: # add hotkey tab
            if True: # input splitter
                tab = ttk.Frame(tabs, style='Custom.TFrame', padding=5)
                tabs.add(tab, text="Add Hotkey")

                frame = ttk.Frame(tab, style='Custom.TFrame')
                frame.pack(fill='x')

                frameleft = ttk.Frame(frame, style='Custom.TFrame')
                frameleft.pack(side=tk.LEFT)
                ttk.Label(frameleft, style="Custom.TLabel", text="Hotkey phrase:").pack(side=tk.TOP)
                # hotkey = ttk.Entry(frameleft, style='Custom.TEntry', justify='center', width=25)

                hotkey = tk.Entry(frameleft, # ttk doesnt have cursor colour options
                                  foreground=dark_text, 
                                  background=dark_bg, 
                                  insertbackground=dark_text,
                                  selectbackground=highlight, 
                                  font=font,
                                  relief='flat',
                                  borderwidth=0, 
                                  justify='center', 
                                  width=25)   
                hotkey.pack(side=tk.TOP, padx=15)

                frameright = ttk.Frame(frame, style='Custom.TFrame')
                frameright.pack(side=tk.RIGHT)
                ttk.Label(frameright, style="Custom.TLabel", text="Hotkey comment:").pack(side=tk.TOP)
                comment = tk.Entry(frameright, # ttk doesnt have cursor colour options
                                  foreground=dark_text, 
                                  background=dark_bg, 
                                  insertbackground=dark_text,
                                  selectbackground=highlight, 
                                  font=font,
                                  relief='flat',
                                  borderwidth=0, 
                                  justify='center', 
                                  width=25)  
                comment.pack(side=tk.TOP, padx=15)

            if True: # link input
                frame = ttk.Frame(tab, style='Custom.TFrame')
                frame.pack(pady=5)

                ttk.Label(frame, style="Custom.TLabel", text="URL or File to open:").pack()

                frame2 = ttk.Frame(frame, style='Custom.TFrame')
                frame2.pack()

                link = tk.Entry(frame2, # ttk doesnt have cursor colour options
                                  foreground=dark_text, 
                                  background=dark_bg, 
                                  insertbackground=dark_text,
                                  selectbackground=highlight, 
                                  font=font,
                                  relief='flat',
                                  borderwidth=0, 
                                  justify='center', 
                                  width=40)  
                link.pack(side=tk.LEFT)
                ttk.Button(frame2, text="Browse", style='Custom.TButton', command=lambda: browse_file(link)).pack(side=tk.LEFT)

            if True: # add button
                frame = ttk.Frame(tab, style='Custom.TFrame')
                frame.pack(padx=12, pady=10, fill='x')
                ttk.Button(frame, text="Add Hotkey", style='Custom.TButton', command=lambda: add_hotkey(hotkey.get(), comment.get(), link.get())).pack(fill='x')

        if True: # app settings hotkey tab
            tab = ttk.Frame(tabs, style='Custom.TFrame')
            tabs.add(tab, text="App Settings")

            frame = ttk.Frame(tab, style='Custom.TFrame')
            frame.pack(padx=15, pady=20, fill='x')

            frame2 = ttk.Frame(frame, style='Custom.TFrame')
            frame2.pack(pady=12, fill='x')
            ttk.Button(frame2, text="Terminate App", style='Custom.TButton', command=lambda: terminate()).pack(fill='x')
            ttk.Label(frame2, style="Custom.TLabel", font=('Segoe UI', 8), foreground=dark_text, text="stops running current instance").pack()

            frame2 = ttk.Frame(frame, style='Custom.TFrame')
            frame2.pack(pady=12, fill='x')
            ttk.Button(frame2, text="Uninstall", style='Custom.TButton', command=lambda: uninstall()).pack(fill='x')
            ttk.Label(frame2, style="Custom.TLabel", font=('Segoe UI', 8), foreground=dark_text, text="uninstalls the app and its contents").pack()
            
    tabs.pack(fill="both", expand=True, padx=5, pady=5)
    root.mainloop()