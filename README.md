# Personal Sound Archive - Team OGGS

## Team Members
- Oliver
- Grant
- Gabe
- Steven

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


Features:
- transcribe text to audio
- metadata / tagging
- searching
- sorting 
- duplicate audio file
- basic graphic interface
- play backwards
- play clips by timecode
- record audio
- filters w/ customization

Contributions: 
Oliver:

Grant:

Gabe:
  I got playing it backward to work, creating a sped-up version of a file, duplicating a file, recording new audio from an input, and trimming a file at certain specified points. I also added some helper functions such as check_inputs and check_length which are there to beable to check certain things
Steven:


### Epoch 3: Advanced Extensions
- **Possible Extensions**:
  - Automated sound classification using machine learning.
  - Graphical User Interface (GUI) for easier interaction.
  - Features for adding/recording new sounds.
  - Web interface for remote access and browsing.
