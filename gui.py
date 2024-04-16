import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from audio import AudioEffects, Recorder
from file_system import FileManager
from sql_commands import databaseManager
from database_init import init


class gui():
    def __init__(self):
        self.root = tk.Tk()

        style = ttk.Style(self.root)

        frame = ttk.Frame(self.root)
        frame.pack()

        widgets_frame = ttk.LabelFrame(frame, text="Insert Row")
        widgets_frame.grid(row=0, column=0, padx=20, pady=10)

        name_entry = ttk.Entry(widgets_frame)
        name_entry.insert(0, "Name")
        name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
        name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")


        button = ttk.Button(widgets_frame, text="Insert")
        button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        button = ttk.Button(widgets_frame, text="Insert")
        button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        separator = ttk.Separator(widgets_frame)
        separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

        treeFrame = ttk.Frame(frame)
        treeFrame.grid(row=0, column=1, pady=10)
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")

        cols = ("Name", "Age", "Subscription", "Employment")
        treeview = ttk.Treeview(treeFrame, show="headings",
                                yscrollcommand=treeScroll.set, columns=cols, height=13)

        treeview.column("Name", width=100)
        treeview.column("Age", width=50)
        treeview.column("Subscription", width=100)
        treeview.column("Employment", width=100)
        treeview.pack()
        treeScroll.config(command=treeview.yview)


        self.audio = AudioEffects()
        self.files = FileManager()
        init()
        self.recorder=Recorder()
        self.db = databaseManager()
        #for development purposes, populate database with example files
        self.db.add_all()

        self.root.mainloop()
                
    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Wave files", "*.wav"), ("MP3 Files", "*.MP3")]
        )
        if not filepath:
            return
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            file = input_file.read()
        self.root.title(f"Simple Text Editor - {filepath}")
    
    def all_files(self):
        self.db.list_tags





