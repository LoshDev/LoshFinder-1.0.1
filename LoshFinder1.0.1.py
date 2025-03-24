import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from threading import Thread
from tkinter import ttk

#APP graphique
class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LoshFinder  V 1.0.1")
        self.root.minsize(750, 450)  
        self.configure_dark_theme()  
        self.create_widgets()
        self.configure_grid()  

    #DARK THEME 
    def configure_dark_theme(self):
       
        self.bg_color = "#2b2b2b" 
        self.fg_color = "white"    
        self.highlight_bg = "yellow"  
        self.highlight_fg = "black"   

  
        self.root.configure(bg=self.bg_color)
        self.root.option_add('*background', self.bg_color)
        self.root.option_add('*foreground', self.fg_color)
        self.root.option_add('*highlightBackground', self.bg_color)  
        self.root.option_add('*highlightColor', self.fg_color)

       
        self.style = ttk.Style()
        self.style.configure('TListbox', background=self.bg_color, foreground=self.fg_color, borderwidth=1, relief='solid')

    def configure_grid(self):
       
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def create_widgets(self):
       
        self.folder_label = tk.Label(self.root, text="Dossier :")
        self.folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        
        self.folder_entry = tk.Entry(self.root, width=50)
        self.folder_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        
        self.browse_button = tk.Button(self.root, text="Parcourir", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

       
        self.search_label = tk.Label(self.root, text="Rechercher :")
        self.search_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

       
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

       
        self.search_button = tk.Button(self.root, text="Rechercher", command=self.start_search)
        self.search_button.grid(row=1, column=2, padx=10, pady=10)

       
        self.file_listbox = tk.Listbox(self.root, width=40, height=20, bd=1, relief=tk.SOLID, highlightthickness=1, highlightcolor=self.highlight_bg, highlightbackground=self.bg_color)
        self.file_listbox.grid(row=2, column=0, padx=10, pady=10, sticky="ns")
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

     
        self.result_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.result_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

    
        self.result_text.config(bg=self.bg_color, fg=self.fg_color)
        self.result_text.tag_config('highlight', background=self.highlight_bg, foreground=self.highlight_fg)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)

    def start_search(self):
        folder = self.folder_entry.get()
        query = self.search_entry.get()

        if not folder or not query:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier et entrer une recherche.")
            return

        self.result_text.delete(1.0, tk.END)  
        self.clear_highlight()  

        self.result_text.insert(tk.END, "Recherche en cours...\n")
        self.root.update()  

       
        search_thread = Thread(target=self.search_in_files, args=(folder, query))
        search_thread.start()

    def search_in_files(self, folder, query):
        self.results = {}  
        files_count = 0
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding='utf-8') as f:
                            for line in f:
                                if query.lower() in line.lower():
                                    if file not in self.results:
                                        self.results[file] = []
                                    self.results[file].append(line.strip())
                    except UnicodeDecodeError:
                        continue
                    files_count += 1
                    if files_count % 10 == 0:
                        self.root.update() 
        if not self.results:
            self.result_text.insert(tk.END, "Rien n'as été trouvé.\n")
        else:
            self.file_listbox.delete(0, tk.END)
            self.file_listbox.insert(tk.END, "Tout")
            for file in self.results:
                self.file_listbox.insert(tk.END, file)

        self.result_text.insert(tk.END, "Recherche terminée.\n")
        self.root.update()  

        self.display_results("Tout")

    def display_results(self, file_key):
        self.result_text.delete(1.0, tk.END)  
        if file_key == "Tout":
            for file in self.results:
                for result in self.results[file]:
                    self.result_text.insert(tk.END, result + "\n")
        else:
            for result in self.results[file_key]:
                self.result_text.insert(tk.END, result + "\n")
        self.apply_highlight(self.search_entry.get())

    def apply_highlight(self, query):
        start_idx = "1.0"
        while True:
            start_idx = self.result_text.search(query, start_idx, tk.END, nocase=1)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(query)}c"
            self.result_text.tag_add('highlight', start_idx, end_idx)
            start_idx = end_idx

    def clear_highlight(self):
        self.result_text.tag_remove('highlight', '1.0', tk.END)
    def on_file_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            file_key = event.widget.get(index)
            self.display_results(file_key)

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
