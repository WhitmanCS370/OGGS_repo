import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from audio import AudioEffects, Recorder
from file_system import FileManager
from sql_commands import databaseManager
from database_init import init


class gui():
    def __init__(self):
        self.audio = AudioEffects()
        self.files = FileManager()
        init()
        self.recorder=Recorder()
        self.db = databaseManager()
        #for development purposes, populate database with example files
        self.db.add_all()
        self.root = tk.Tk()
        self.root.title("Audio Manager")
        style = ttk.Style(self.root)

        frame = ttk.Frame(self.root)
        frame.pack()

        widgets_frame = ttk.LabelFrame(frame, text="Insert Row")
        widgets_frame.grid(row=0, column=0, padx=20, pady=10)

        name_entry = ttk.Entry(widgets_frame)
        name_entry.insert(0, "Name")
        name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
        name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

        button = ttk.Button(widgets_frame, text="play")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        button = ttk.Button(widgets_frame, text="Backward")
        button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        button = ttk.Button(widgets_frame, text="Speed Up")
        button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        separator = ttk.Separator(widgets_frame)
        separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

        treeFrame = ttk.Frame(frame)
        treeFrame.grid(row=0, column=1, pady=10)
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")

        cols = ("Title", "Artist", "Album", "Genre", "Filepath", "Duration")
        treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        treeview.heading("#0",text="File")
        treeview.heading("Title", text="Title")
        treeview.heading("Artist", text="Artist")
        treeview.heading("Album", text="Album")
        treeview.heading("Genre", text="Genre")
        treeview.heading("Filepath", text="Filepath")
        treeview.heading("Duration", text="Duration")
        
        for item in self.db.list_files():
            filepath=self.db.get_filepath(item)
            treeview.insert("",tk.END,text="File",values=(item,self.db.get_artist(item),self.db.get_album(item),self.db.get_genre(item),filepath,self.db.get_duration(filepath)))
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





