import tkinter as tk
from tkinter import ttk,Label, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from logic import AudioEffects, Recorder, Logic
from file_system import FileManager
from sql_commands import databaseManager
from database_init import init, init_default_tags
from RangeSlider.RangeSlider import RangeSliderH
import threading
import queue

from os import path

class mainWindow():
    def __init__(self,root):
        if not path.isfile('./audio_library.sqlite'):
            init()
            init_default_tags()
        db = databaseManager()
        self.audio = AudioEffects(db)
        self.files = FileManager()
        self.recorder=Recorder(db)
        self.logic=Logic(db)

        self.root=root
        #for development purposes, populate database with example files

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

        name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
        name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")
        
        playlist_frame = ttk.Frame(showing_frame)
        playlist_frame.grid(row=2, column=0)
        lbl=tk.Label(playlist_frame,text="Playlists:")
        lbl.grid(row=0,column=0, padx=5, pady=3,sticky="nw")
        n = tk.StringVar() 
        playlist_dropdown = ttk.Combobox(playlist_frame, width = 27, textvariable = n) 
        playlist_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        options = self.logic.get_playlist_list()
        playlist_dropdown['values'] = tuple(options)
        playlist_dropdown.bind("<<ComboboxSelected>>", lambda x:self.logic.show_playlist(playlist_dropdown, treeview))
        create_playlist=ttk.Button(showing_frame,text="Create Playlist", command=lambda:[self.add_playlist_popup(playlist_dropdown)])
        create_playlist.grid(row=3,column=0,padx=5, pady=3, sticky="nsew")
        
        add_to_playlist=ttk.Button(showing_frame,text="Add To Playlist", command=lambda:[self.to_playlist_popup(self.get_selected_filepaths(treeview))])
        add_to_playlist.grid(row=4,column=0,padx=5, pady=3, sticky="nsew")
        
        play_button = ttk.Button(showing_frame, text="Play",command=lambda:[self.audio.sequence(self.get_selected_filepaths(treeview))])
        play_button.grid(row=6, column=0, padx=5, pady=3, sticky="nsew")
        
        layer_button = ttk.Button(showing_frame, text="Layer",command=lambda:self.audio.layer(self.get_selected_filepaths(treeview)))
        layer_button.grid(row=8, column=0, padx=5, pady=3, sticky="nsew")
        
        delete_button = ttk.Button(showing_frame, text="Delete",command=lambda:[self.logic.delete_file_with_name(name_entry.get()),self.files.delete_file(name_entry.get()),self.logic.input_files(treeview)])
        delete_button.grid(row=9, column=0, padx=5, pady=3, sticky="nsew")
        
        rename_button = ttk.Button(showing_frame, text="Rename",command=lambda:[self.rename_popup(name_entry),self.logic.input_files(treeview)])
        rename_button.grid(row=10,column=0,padx=5,pady=3, sticky="nsew")
        
        speed_Up_button = ttk.Button(showing_frame, text="Speed Up",command=lambda:[self.speed_up_popup(name_entry),self.logic.input_files(treeview)])
        speed_Up_button.grid(row=11, column=0, padx=5, pady=3, sticky="nsew")
        
        backward_button = ttk.Button(showing_frame, text="Backward",command=lambda:[self.logic.add_file(self.audio.backward(name_entry)),self.logic.input_files(treeview)])
        backward_button.grid(row=12, column=0, padx=5, pady=5, sticky="nsew")

        distortion_button = ttk.Button(showing_frame, text="Distort", command=lambda: [(self.audio.apply_distortion(name_entry)), self.logic.input_files(treeview)])
        distortion_button.grid(row=19, column=0, padx=5, pady=5, sticky="nsew")
        
        record_button = ttk.Button(showing_frame, text="Record",command=lambda:[self.record_popup(name_entry)])
        record_button.grid(row=13, column=0, padx=5, pady=3, sticky="nsew")
        
        trim_button = ttk.Button(showing_frame, text="Trim",command=lambda:[self.trim_popup(name_entry)])
        trim_button.grid(row=14, column=0, padx=5, pady=3, sticky="nsew")
        
        add_file_button = ttk.Button(showing_frame, text="Add File",command=lambda:[self.add_file_popup(name_entry)])
        add_file_button.grid(row=15, column=0, padx=5, pady=5, sticky="nsew")
        
        duplicate_file_button = ttk.Button(showing_frame, text="Duplicate File",command=lambda:[self.files.duplicate_file(name_entry.get(), db)])
        duplicate_file_button.grid(row=16, column=0, padx=5, pady=3, sticky="nsew")
        
        add_tag_button = ttk.Button(showing_frame, text="Add Tag",command=lambda:[self.add_tag_popup(name_entry)])
        add_tag_button.grid(row=17, column=0, padx=5, pady=3, sticky="nsew")
        
        delete_tag_button = ttk.Button(showing_frame, text="Delete Tag",command=lambda:[self.delete_tag_popup(name_entry)])
        delete_tag_button.grid(row=18, column=0, padx=5, pady=3, sticky="nsew")
    
        
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=0, column=1, pady=10,sticky=tk.NSEW)
        root.rowconfigure(1, weight=1)

        
        tree_details_frame=ttk.Frame(tree_frame,border=2,)
        tree_details_frame.pack(side="top",fill="x")
        
        file_label=ttk.Label(tree_details_frame,text="All Files:")
        file_label.pack(side="left",anchor="w")
        
        refresh_button=ttk.Button(tree_details_frame,text="refresh",command=lambda: self.logic.input_files(treeview))
        refresh_button.pack(side="right",anchor="e")
        
        treeScroll = ttk.Scrollbar(tree_frame)
        treeScroll.pack(side="right", fill="y")

        cols = ("Title", "Filepath","Tags", "Duration")
        treeview = ttk.Treeview(tree_frame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        treeview.heading("#0",text="File")
        treeview.heading("Title", text="Title")
        treeview.heading("Tags", text = "Tags")
        treeview.heading("Filepath", text="Filepath")
        treeview.heading("Duration", text="Duration")
        
        treeview.bind('<ButtonRelease-1>', lambda event :[self.selectItem(treeview,name_entry)])
        

        self.logic.input_files(treeview)
        
        treeview.pack(fill="both", expand=1)
        treeScroll.config(command=treeview.yview)


        #for development purposes, populate database with example files

        self.root.mainloop()
        
    def rename_popup(self, entry):
        try:
            if len(entry)==0:
                self.select_files_popup()
                return
            self.top=Toplevel(self.root)
            self.top.geometry('300x300')
            self.pathing = path
            rename_Frame = ttk.Frame(self.top)
            rename_Frame.pack()
            lbl=tk.Label(rename_Frame,text="Enter New filename")
            lbl.grid(row=0,column=0, padx=5, pady=5,sticky="n")
            rename_entry=tk.Entry(rename_Frame)
            rename_entry.grid(row=1,column=0,padx=5,pady=5,sticky="n")
            rename_button=tk.Button(rename_Frame,text='Rename',command=lambda:[self.rename_file(rename_entry,entry.get()+".wav"), self.cleanup(self.top)])
            rename_button.grid(row=2,column=0,padx=5,pady=5,sticky="n")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def cleanup(self,win):
        win.destroy()
        
    def rename_file(self,entry,oldFileName):
        print("rename file called")
        newFileName = entry.get()+".wav"
        print(oldFileName, newFileName)
        self.files.rename_file(oldFileName,newFileName) #first, rename the actual file
        self.logic.rename(newFileName,oldFileName)
        self.top.destroy()
        
    def speed_up_popup(self, entry):
        try:
            if len(entry.get())==0:
                self.select_files_popup()
                return
            entry_value=entry.get()
            print(type(entry_value))
            self.top=Toplevel(self.root)
            self.top.geometry('400x300')
            speed_up_Frame = ttk.Frame(self.top)
            speed_up_Frame.pack()
            lbl=tk.Label(speed_up_Frame,text="How much do you want to speed it up by?(needs to be numeric)")
            lbl.grid(row=0,column=0, padx=5, pady=5,sticky="n")
            amount_entry = ttk.Entry(speed_up_Frame,width=10)
            amount_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
            sp_popup_button=tk.Button(speed_up_Frame,text='Speed Up',command=lambda:[self.logic.add_filepath_speed_up(entry,amount_entry), self.cleanup(self.top)])
            sp_popup_button.grid(row=2,column=0,padx=5,pady=5,sticky="n")
        except Exception as e:
            print(f"An error occurred: {e}")


    def record_popup(self, entry):
        try:
            self.top=Toplevel(self.root)
            self.top.geometry('300x300')
            record_Frame = ttk.Frame(self.top)
            record_Frame.pack()
            lbl=tk.Label(record_Frame,text="Enter New filename")
            lbl.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            amount_entry = ttk.Entry(record_Frame,width=10)
            amount_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
            amount_entry.insert(0,"file")
            timer_Label=tk.Label(record_Frame,text="timer")
            timer_Label.grid(row=2,column=0, sticky="n")
            rec_popup_button=tk.Button(record_Frame, text='Record',command = lambda:[self.recorder.click_handler(rec_popup_button,amount_entry.get(),timer_Label)])
            rec_popup_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        except Exception as e:
            print(f"An error occurred: {e}")
            



    def to_playlist_popup(self, entry):
        try:
            if len(entry)==0:
                self.select_files_popup()
                return
            self.top=Toplevel(self.root)
            self.top.geometry('300x300')
            playlist_Frame = ttk.Frame(self.top)
            playlist_Frame.pack()
            lbl=tk.Label(playlist_Frame,text="Add file to playlist")
            lbl.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            n = tk.StringVar() 
            playlist_dropdown = ttk.Combobox(playlist_Frame, width = 27, textvariable = n) 
            playlist_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            options = self.logic.get_playlist_list()
            playlist_dropdown['values'] = tuple(options)
            playlist_popup_button=tk.Button(playlist_Frame, text='Add',command = lambda:[self.logic.song_playlist(playlist_dropdown,entry), self.cleanup(self.top)])
            playlist_popup_button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        except TypeError:
            print("error occured: Select file to add")
        
    def add_playlist_popup(self,playlist_dropdown):
        try:
            self.top=Toplevel(self.root)
            self.top.geometry('300x300')
            playlist_Frame = ttk.Frame(self.top)
            playlist_Frame.pack()
            name_entry=tk.Label(playlist_Frame,text="What is the playlist's name?")
            name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            playlist_entry = ttk.Entry(playlist_Frame,width=10)
            playlist_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
            playlist_popup_button=tk.Button(playlist_Frame, text='Add',command = lambda:[self.logic.create_playlist(playlist_entry),self.update_playlist_list(playlist_dropdown), self.cleanup(self.top)])
            playlist_popup_button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def trim_popup(self,entry,treeview):
        try:
            self.top=Toplevel(self.root)
            self.top.geometry('450x300')
            trim_Frame = ttk.Frame(self.top)
            trim_Frame.pack()
            name_entry=tk.Label(trim_Frame,text="trim it?")
            name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            duration=treeview.item(entry.get())['values'][3]
            hLeft = tk.DoubleVar()  #left handle variable initialised to value 0
            hRight = tk.DoubleVar()  #right handle variable initialised to duration of file
            hSlider = RangeSliderH( trim_Frame , [hLeft, hRight], min_val=0, max_val=duration, padX=96.76 ,step_marker = True, step_size = duration/10)   #horizontal slider
            hSlider._RangeSliderH__moveBar(0, 0.0)   # 0.2 means 20 for range 0 to 100
            hSlider._RangeSliderH__moveBar(1, 1.0)   # 0.8 means 80 for range 0 to 100
            hSlider.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
            playlist_popup_button=tk.Button(trim_Frame, text='Trim',command = lambda:[self.logic.add_filepath_trim(entry,hLeft,hRight,self.audio), self.cleanup(self.top)])
            playlist_popup_button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        except TypeError:
            self.select_files_popup()
        except Exception as e:
            print(f"exception occured: {e}")

        
    def add_file_popup(self):
        filepath = askopenfilename()  # Open file dialog to choose a file
        if filepath:
            moved_filepath = self.files.add_file(filepath)
            self.logic.add_filepath(moved_filepath)
            print('File added successfully')
        
    def duplicate_file_popup(self,entry):
        print('dup file')
    
    def add_tag_popup(self,entry):
        print('add Tag')
        
    def delete_tag_popup(self,entry):
        print('delete_tag')
        
    def select_files_popup(self):
        try:
            top=Toplevel(self.root)
            top.geometry('450x300')
            trim_Frame = ttk.Frame(top)
            trim_Frame.pack()
            name_entry=tk.Label(trim_Frame,text="You didn't select any files")
            name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        except Exception as e:
            print(f"exception occured: {e}")
        

    def update_playlist_list(self,dropdown):
        try:
            options = self.logic.get_playlist_list()
            dropdown['values'] = tuple(options)
        except:
            print("failed to update playlist")
        
    def get_selected_filepaths(self,treeview):
        filepathList=[]
        curItems = treeview.selection()
        curItems=list(curItems)
        for item in curItems:
            filepathList.append(str(treeview.item(item)['values'][1]))

        return filepathList
    
    def get_selected_filenames(self,treeview):
        filepathList=[]
        curItems = treeview.selection()
        curItems=list(curItems)
        for item in curItems:
            filepathList.append(str(treeview.item(item)['values'][0]))
        return filepathList
    
            
    def selectItem(self, treeview, name_entry):
        try:
            curItem = treeview.focus()
            name_entry.delete(0,tk.END)
            name_entry.insert(0, treeview.item(curItem)['values'][0])
        except IndexError:
            print("click again")
     
    def show_playlist(self,playlist_dropdown,treeview):
        if (playlist_dropdown.get() == ""):
            self.input_files(treeview)
            return
        for item in treeview.get_children():
            treeview.delete(item)
        files=self.db.get_playlist(playlist_dropdown.get())
        for i in range(len(files)):
            title = files[i].split("/")[-1].split(".")[0]
            treeview.insert("",tk.END,text=f"Item #{i+1}",values=(title,files[i],self.db.tags_from_file(title),self.db.get_duration(files[i])))
    
    def all_files(self):
        self.db.list_tags

def open_gui():
    root = tk.Tk()
    m=mainWindow(root)
