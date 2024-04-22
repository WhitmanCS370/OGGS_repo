import tkinter as tk
from tkinter import ttk,Label
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
        
        left_frame = ttk.Frame(frame)
        left_frame.grid(row=0, column=0)

        showing_frame = ttk.LabelFrame(left_frame, text="Showing")
        showing_frame.grid(row=0, column=0, padx=20, pady=10)
        
        name_entry = ttk.Entry(showing_frame)
        name_entry.insert(0, "File Name")
        name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
        name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")
        
        playlist_frame = ttk.Frame(showing_frame)
        playlist_frame.grid(row=2, column=0)
        lbl=tk.Label(playlist_frame,text="Playlists:")
        lbl.grid(row=0,column=0, padx=5, pady=5,sticky="nw")
        n = tk.StringVar() 
        monthchoosen = ttk.Combobox(playlist_frame, width = 27, textvariable = n) 
        monthchoosen.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        monthchoosen['values'] = (self.db.list_playlists())
        
        button = ttk.Button(showing_frame, text="play",command=lambda:[self.audio.set_currently_playing_file(name_entry.get()),self.audio.play(name_entry.get())])
        button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # separator = ttk.Separator(showing_frame)
        # separator.grid(row=6, column=0, padx=(20, 10), pady=10, sticky="ew")
        
        
        creating_frame = ttk.LabelFrame(left_frame, text="Create Files")
        creating_frame.grid(row=1, column=0, padx=20, pady=10)
        
        button = ttk.Button(creating_frame, text="Backward",command=lambda:[self.audio.backward(name_entry.get()),self.input_files()])
        button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        button = ttk.Button(creating_frame, text="Speed Up",command=lambda:[self.audio.speed_up(name_entry.get()),self.input_files()])
        button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=0, column=1, pady=10)
        
        treeScroll = ttk.Scrollbar(tree_frame)
        treeScroll.pack(side="right", fill="y")

        cols = ("Title", "Artist", "Album", "Genre", "Filepath", "Duration")
        treeview = ttk.Treeview(tree_frame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        treeview.heading("#0",text="File")
        treeview.heading("Title", text="Title")
        treeview.heading("Artist", text="Artist")
        treeview.heading("Album", text="Album")
        treeview.heading("Genre", text="Genre")
        treeview.heading("Filepath", text="Filepath")
        treeview.heading("Duration", text="Duration")
        
        treeview.bind('<ButtonRelease-1>', lambda event:self.selectItem(event,treeview,name_entry))
        

        self.input_files(treeview)
        
        treeview.pack()
        treeScroll.config(command=treeview.yview)


        #for development purposes, populate database with example files
        self.db.add_all()

        self.root.mainloop()
    
    def input_files(self,treeview):
        files=self.db.list_files()
        for i in range(len(files)):
            filepath=self.db.get_filepath(files[i])
            treeview.insert("",tk.END,text=f"Item #{i+1}",values=(files[i],self.db.get_artist(files[i]),self.db.get_album(files[i]),self.db.get_genre(files[i]),filepath,self.db.get_duration(filepath)))
    
    def selectItem(self,a,treeview,name_entry):
        try:
            curItem = treeview.focus()
            name_entry.delete(0,tk.END)
            name_entry.insert(0, treeview.item(curItem)['values'][0])

        except IndexError:
            print("click again")
              
    
    def all_files(self):
        self.db.list_tags





