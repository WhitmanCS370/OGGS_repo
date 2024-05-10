


# Personal Sound Archive - Team OGGS






## Team Members
- Oliver
- Grant
- Gabe
- Steven


# Setup:
1. Clone this repository onto your computer.
2. make sure that python is installed, type "python --version" to make sure 
3. Navigate to the program directory.
4. Create virtual python environment and set it as your python source.
5. install dependencies with "pip install -r requirements.txt"



# Program Usage: GUI

## To start the program:
1. navigate to the project directory
2. run "python main.py -g" in the command line

## To use program:
1. Use buttons in gui to perform actions
2. To manipulate or play files, select them in the window and use buttons to perform actions.



# Program Usage: CLI

## To start the program:
  1. navigate into the directory that this program is stored in
  2. run "python main.py" in command line
  
## To play a files:
  1. If you do not know the name of the file or playlist you want to play, run list_files or list_playlists
  2. In the program's command line interface, type play <filename> or play -p <playlist>, in the case of filename, do not include file extensions. 

## To find out the functionality of other commands
  - Type "help" or "help <command_name>" for specific command usage





## Project Overview
As a part of CS370 - Software Design at Whitman College, our team will be working on this semester-long project creating a personal sound archive in Python.

With the ubiquity of mobile technology and cloud storage, many of us have amassed huge digital photo archives documenting personal moments both meaningful and mundane. Yet these digital archives are oddly silent: You might have hundreds of photos of your dog, but to hear her bark you must conjure it from memory. How might developing a sonic archive, focused on personally relevant everyday sounds, reinvent our relationships with sound and encourage everyday sonic thinking?

A personal sound archive is highly complex with many possible features: managing the data and metadata associated with the sounds, organizing the sounds, providing ways for users to browse and listen to sounds, adding new sounds to the archive, remixing the sounds, sharing the sounds, and more. Your project will focus on a subset of these features.
Project epochs

Our project will be divided into three main epochs that tackle specific features of developing a personal sound archive: 

### Epoch 1: Basic Sound Browsing and Playback
- **Functionality**:
  - Browse a list of available sounds.
  - Play back single or multiple sounds simultaneously.
  - Play a sequence of sounds.
  - Rename sounds within the archive.
- **Technology**: Python, simpleaudio library.

Contributions: 
Oliver:
  worked on getting the file manager and the interface to work so that we can parse the arguments and rename files and stuff like that.
Grant:
  worked on original argparser that ended up turning in to our current command line interface, created unittests
Gabe:
  worked on getting layering and playing to work as well as ended up not being able to get sequencing to work(had someone else take a look).
Steven:


### Epoch 2: Enhanced Listening and Sound Organization
- **Functionality**:
  - Advanced playback options (e.g., playing sounds backward, random snippets).
  - Light sound editing and filtering.
  - Organize sounds with a database, including tagging and metadata updates.
- **Tools**: Selection of appropriate Python libraries.


Use cases for epoch two:
- audio manipulation program
- find satanic messages in audio
- catagorization and classification of audio


New Features:
- metadata / tagging
- create playlists
- sort by tag
- duplicate audio file
- play backwards
- speed up audio files
- record audio
- trim audio files 


Contributions: 
Oliver:
  I wrote the new interface, sql commands, and rewrote the audio handler to use pydub instead of simpleaudio. This allowed us to implement features like pausing / playing audio, creating and playing playlists, adding tags to specific files, and having a constant command line interface to use the program. 

Grant:

Gabe:
  I got playing it backward to work, creating a sped-up version of a file, duplicating a file, recording new audio from an input, and trimming a file at certain specified points. I also added some helper functions such as check_inputs and check_length which are there to beable to check certain things

Steven:
  Changes to sql commands, error checking for sql commands and some other functions. Unified file system handling to make sure there's only one folder being used. Created a separate implementation of the audio player and CLI using pyaudio as pydubs doesn't want to work properly on Windows. The separate audio player has streaming, pause/play/stop implemented.

### Epoch 3: Advanced Extensions
- **Possible Extensions**:
  - Automated sound classification using machine learning.
  - Graphical User Interface (GUI) for easier interaction.
  - Features for adding/recording new sounds.
  - Web interface for remote access and browsing.



Oliver Baltzer: I worked on implementing each existing feature with the new GUI and fixed bugs as they came up, I also implemented the system for automatic tagging. 

Steven Lin: I worked on reworking audio player, fixing issues that caused audio to be inconsistent across different OS, and implementing pause/play/skip functions.

Gabriel Paris-Moe: I did the main design and implementation of the GUI as well as making many of the popups and making the original functions that we already had work with the popup.

Grant Didway: I worked on the distort feature and making popup windows that pass the correct information to logic.py, path consistency accross different operating systems, and fixing issues with tagging.
