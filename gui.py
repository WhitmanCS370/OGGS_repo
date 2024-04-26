import tkinter as tk
from tkinter import ttk,Label, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from audio import AudioEffects, Recorder
from file_system import FileManager
from sql_commands import databaseManager
from database_init import init
from threading import Timer
from os import path
    
class RenameWindow(object):
    def __init__(self,master,db,fileManager,oldFileName):
        self.pathing = path
        self.master=master
        self.top=Toplevel(master)
        self.top.geometry('300x300')
        lbl=tk.Label(self.top,text="Enter New filename")
        lbl.grid(row=0,column=0, padx=5, pady=5,sticky="nsew")
        self.e=tk.Entry(self.top)
        self.e.grid(row=1,column=0,padx=5,pady=5,sticky="nsew")
        self.b=tk.Button(self.top,text='Rename',command=lambda:[self.rename_file(db,fileManager,oldFileName)])
        self.b.grid(row=2,column=0,padx=5,pady=5,sticky="nsew")
        if oldFileName==None:
            self.cleanup()
        
    def cleanup(self):
        self.top.destroy()
        
    def rename_file(self,db,fileManager,oldFileName):
        print("rename file called")
        newFileName = self.e.get()+".wav"
        print(oldFileName, newFileName)
        fileManager.rename_file(oldFileName,newFileName) #first, rename the actual file
        db.add_from_file(self.pathing.join(self.pathing.curdir, "sounds", newFileName))
        db.delete_file_by_name(oldFileName[:-4])
        self.value=True
        self.top.destroy()
        


class mainWindow():
    def __init__(self,root):
        self.audio = AudioEffects()
        self.files = FileManager()
        self.recorder=Recorder()
        self.db = databaseManager()
        init()
        self.root=root
        #for development purposes, populate database with example files
        self.db.add_all()

        self.root.title("Audio Manager")
        self.root.config(height=700)
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
        dropdown = ttk.Combobox(playlist_frame, width = 27, textvariable = n) 
        dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        dropdown['values'] = (self.db.list_playlists())
        create_playlist=ttk.Button(showing_frame,text="Create Playlist", command=lambda:[self.db.add_playlist(name_entry.get()),self.update_playlist_list(dropdown),self.rename])
        create_playlist.grid(row=3,column=0,padx=5, pady=5, sticky="nsew")
        
        play_Button = ttk.Button(showing_frame, text="Play",command=lambda:[self.playSequence(self.get_selected_filepaths(treeview))])
        play_Button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        
        sequence_Button = ttk.Button(showing_frame, text="Sequece",command=lambda:self.audio.sequence(self.get_selected_filepaths(treeview)))
        sequence_Button.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        
        layer_Button = ttk.Button(showing_frame, text="Layer",command=lambda:self.audio.layer(self.get_selected_filepaths(treeview)))
        layer_Button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        
        delete_Button = ttk.Button(showing_frame, text="Delete",command=lambda:[self.db.delete_file_by_name(name_entry.get()),self.files.delete_file(name_entry.get()),self.input_files(treeview)])
        delete_Button.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")
        
        rename_Button = ttk.Button(showing_frame, text="Rename",command=lambda:[self.renamePopup(name_entry),self.input_files(treeview)])
        rename_Button.grid(row=9,column=0,padx=5,pady=5, sticky="nsew")
        

        creating_frame = ttk.LabelFrame(left_frame, text="Create Files")
        creating_frame.grid(row=1, column=0, padx=20, pady=10)
        
        backward_Button = ttk.Button(creating_frame, text="Backward",command=lambda:[self.db.add_from_file(self.audio.backward(self.db.get_filepath(name_entry.get()))),self.input_files(treeview)])
        backward_Button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        speed_Up_Frame = ttk.Frame(creating_frame)
        speed_Up_Frame.grid(row=2, column=0)
        amount_entry = ttk.Entry(speed_Up_Frame,width=10)
        amount_entry.insert(0, "Amount")
        amount_entry.bind("<FocusIn>", lambda e: amount_entry.delete('0', 'end'))
        amount_entry.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="ew")
        speed_Up_Button = ttk.Button(speed_Up_Frame, text="Speed Up",command=lambda:[self.db.add_from_file(self.audio.speed_up(self.db.get_filepath(name_entry.get()),amount_entry.get())),self.input_files(treeview)])
        speed_Up_Button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=0, column=1, pady=10)
        
        tree_details_frame=ttk.Frame(tree_frame,border=2,)
        tree_details_frame.pack(side="top")
        
        file_label=ttk.Label(tree_details_frame,text="All Files")
        file_label.pack(side="left",anchor="w")
        
        refresh_button=ttk.Button(tree_details_frame,text="refresh",command=lambda: self.input_files(treeview))
        refresh_button.pack(side="right",anchor="e")
        
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
        
        treeview.bind('<ButtonRelease-1>', lambda event :[self.selectItem(treeview,name_entry)])
        

        self.input_files(treeview)
        
        treeview.pack()
        treeScroll.config(command=treeview.yview)


        #for development purposes, populate database with example files
        self.db.add_all()

        self.root.mainloop()
        
    def test(self, entry):
        self.top=Toplevel(self.root)
        self.top.geometry('300x300')
        lbl=tk.Label(self.top,text="Enter New filename")
        lbl.grid(row=0,column=0, padx=5, pady=5,sticky="nsew")
        self.e=tk.Entry(self.top)
        self.e.grid(row=1,column=0,padx=5,pady=5,sticky="nsew")
        self.b=tk.Button(self.top,text='Rename',command=lambda:[self.rename_file(entry.get()+".wav")])
        self.b.grid(row=2,column=0,padx=5,pady=5,sticky="nsew")
        if entry.get()+".wav"==None:
            self.cleanup()
        
    def cleanup(self):
        self.top.destroy()
        
    def rename_file(self,oldFileName):
        self.db.rename(oldFileName, self.e.get()+".wav")
        print("rename called")
        self.fileManager.rename_file(oldFileName,self.e.get()+".wav")
        self.top.destroy()
        
    def renamePopup(self,entry):
        try:
            
            self.w=RenameWindow(self.root,self.db,self.files,entry.get()+".wav")
            print("rename")
        except Exception as error:
            print("none selected: ",error)
            
    def playSequence(self,files):
        for file in files:
            self.audio.set_currently_playing_file(file)
            self.audio.play()

    def update_playlist_list(self,dropdown):
        try:
            dropdown['values'] = (self.db.list_playlists()[0])
        except:
            print("failed to update playlist")
        
    def get_selected_filepaths(self,treeview):
        filepathList=[]
        curItems = treeview.selection()
        curItems=list(curItems)
        for item in curItems:
            filepathList.append(str(treeview.item(item)['values'][4]))

        return filepathList
    
    def get_selected_filenames(self,treeview):
        filepathList=[]
        curItems = treeview.selection()
        curItems=list(curItems)
        for item in curItems:
            filepathList.append(str(treeview.item(item)['values'][0]))
        return filepathList
    
    def input_files(self,treeview):
        print()
        for item in treeview.get_children():
            treeview.delete(item)
        files=self.db.list_files()
        print(files)
        for i in range(len(files)):
            filepath=self.db.get_filepath(files[i])
            print(files[i])
            treeview.insert("",tk.END,text=f"Item #{i+1}",values=(files[i],self.db.get_artist(files[i]),self.db.get_album(files[i]),self.db.get_genre(files[i]),filepath,self.db.get_duration(filepath)))

    def selectItem(self,treeview,name_entry):
        try:
            curItem = treeview.focus()
            name_entry.delete(0,tk.END)
            name_entry.insert(0, treeview.item(curItem)['values'][0])

        except IndexError:
            print("click again")
              
    
    def all_files(self):
        self.db.list_tags
        



def open_gui():
    root = tk.Tk()
    m=mainWindow(root)
