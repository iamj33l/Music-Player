"""Simple MP3 Music player in python with GUI"""

# Importing modules

from tkinter import *
from tkinter import filedialog, ttk
import pygame
import os
import time
from mutagen.mp3 import MP3


# Defining MusicPlayer function
def MusicPlayer():
    """This function run the music player"""

    # creating the main frame
    window = Tk()
    window.title('Music Player')
    window.resizable(0, 0)
    window.iconbitmap('music.ico')

    # initializing pygame
    pygame.init()

    # creating menu bar
    menubar = Menu(window)
    window.config(menu=menubar)

    # creating playlist frame
    playlistFrame = Frame(window, bg='#333333', relief=FLAT, width=40, borderwidth=1)
    playlistFrame.pack(side=LEFT, fill=BOTH)

    # creating scrollbar for playlist
    scrollbar = Scrollbar(playlistFrame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # creating playlist box
    songsBox = Listbox(playlistFrame,
                       bg='#333333',
                       fg='#FFFFFF',
                       width=40,
                       selectbackground='#3366FF',
                       selectforeground='#FFFFFF',
                       font=('Inter', 12),
                       relief=FLAT,
                       borderwidth=0,
                       yscrollcommand=scrollbar.set)
    songsBox.pack(side=LEFT, fill=BOTH)

    # function to choose music from any directory
    def choose_directory():
        directory = filedialog.askdirectory()
        os.chdir(directory)
        songList = os.listdir()
        # clear the playlist if there is any song in it
        songsBox.delete(0, END)
        for song in songList:
            if song.endswith('.mp3'):
                # insert songs into playlist
                songsBox.insert(END, song[:-4])

    # creating file menu
    fileMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=fileMenu)

    # adding open option to file menu
    fileMenu.add_command(label='Open', command=choose_directory)

    # creating frame for song details
    songDetailsFrame = Frame(window, relief=FLAT, borderwidth=0)
    songDetailsFrame.pack(side=TOP, pady=4, fill=BOTH)
    
    # function to show help
    def showHelp():
        helpFrame = Tk()
        helpFrame.title("Help")
        helpFrame.geometry('400x500')
        helpFrame.iconbitmap('Help.ico')
        helpFrame.resizable(False, False)

        with open('Help.txt', 'r') as file:
            helpText = file.read()

        scrollBar = Scrollbar(helpFrame)
        scrollBar.pack(side=RIGHT, fill=Y)

        helpContent = Text(helpFrame, wrap=WORD, font='"IBM plex mono" 10', yscrollcommand=scrollBar.set)
        helpContent.insert(END, helpText)
        helpContent.config(state=DISABLED)
        helpContent.pack(side=LEFT, fill=BOTH)
        scrollBar.config(command=helpContent.yview)

    # creating help menu
    helpMenu = Menu(menubar, tearoff=FALSE)
    helpMenu.add_command(label='About', command=showHelp)
    menubar.add_cascade(label='Help', menu=helpMenu)

    # currently playing label
    currentlyPlaying = Label(songDetailsFrame,
                             text='Currently Playing...',
                             font=('Product Sans', 15),
                             justify=CENTER,
                             relief=FLAT,
                             borderwidth=0)
    currentlyPlaying.pack(pady=4)

    # displaying song name
    songName = Label(songDetailsFrame,
                     text="No song selected",
                     font=('Product Sans', 24),
                     justify=CENTER,
                     relief=FLAT,
                     borderwidth=0,
                     wraplength=350)
    songName.pack(pady=4)

    # creating label for song duration
    songDuration = Label(songDetailsFrame,
                         text='0:00 of 0:00',
                         font=('Product Sans', 12),
                         justify=CENTER,
                         relief=FLAT,
                         borderwidth=0)
    songDuration.pack(pady=8)

    # function to get song play time
    def songTime():
        # get current song time
        currentTime = pygame.mixer.music.get_pos() / 1000
        convertedCurrentTime = time.strftime('%M:%S', time.gmtime(currentTime + 1))

        # get song length
        index = songsBox.curselection()
        song = f'{songsBox.get(index)}.mp3'.strip()
        currentSong = MP3(song)
        global songLength
        songLength = currentSong.info.length
        convertedSongLength = time.strftime('%M:%S', time.gmtime(songLength))

        # update song duration label
        songDuration['text'] = f'{convertedCurrentTime} of {convertedSongLength}'

        # update slider position
        songSlider.config(value=int(currentTime))

        # if song is over then change the duration label to 0:00 of 0:00
        # and unselect the song from playlist
        if int(currentTime) + 1 == int(songLength):
            songDuration['text'] = '0:00 of 0:00'
            songSlider.config(value=0)
            songsBox.selection_clear(ACTIVE)

        # call songTime function after 1 second
        songDuration.after(1000, songTime)

    # creating slider for song duration
    songSlider = ttk.Scale(songDetailsFrame,
                           from_=0,
                           to=100,
                           orient=HORIZONTAL,
                           value=0)
    songSlider.pack(padx=20, fill=X)

    # function to play the selected song
    def play():
        # get the song name from playlist and play it
        song = f'{songsBox.get(ACTIVE)}.mp3'.strip()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        songName['text'] = f'{songsBox.get(ACTIVE)}'.strip()

        # call songTime function
        songTime()

        # configure slider
        songSlider.config(to=songLength, value=0)

    # global variable to check if the song is paused or not
    global paused
    paused = False

    # function to pause or unpause the current song
    def pause():
        global paused
        # if song is paused then unpause it and vice versa
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True

    # function to stop the current song and unselect the song from playlist
    def stop():
        # stop the song and unselect the song from playlist
        pygame.mixer.music.stop()
        songsBox.selection_clear(ACTIVE)
        songName['text'] = 'No song selected'

        # clear song duration label
        songDuration['text'] = '0:00 of 0:00'

        # set slider value to 0
        songSlider.config(value=0)

    # function to play the next song in the playlist
    def nextSong():
        nextOne = songsBox.curselection()

        # if the current song is the last song in the playlist then play the first song
        if nextOne[0] == songsBox.size() - 1:
            nextOne = 0

        else:
            nextOne = nextOne[0] + 1

        song = f'{songsBox.get(nextOne)}.mp3'.strip()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        songsBox.selection_clear(0, END)
        songsBox.activate(nextOne)
        songsBox.selection_set(nextOne, last=None)
        songName['text'] = f'{songsBox.get(nextOne)}'.strip()

        # call songTime function
        songTime()

        # configure slider
        songSlider.config(to=songLength, value=0)

    # function to play the previous song in the playlist
    def previousSong():
        previousOne = songsBox.curselection()

        # if the current song is the first song in the playlist then play the last song
        if previousOne[0] == 0:
            previousOne = songsBox.size() - 1
        else:
            previousOne = previousOne[0] - 1
        song = f'{songsBox.get(previousOne)}.mp3'.strip()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        songsBox.selection_clear(0, END)
        songsBox.activate(previousOne)
        songsBox.selection_set(previousOne, last=None)
        songName['text'] = f'{songsBox.get(previousOne)}'.strip()

        # call songTime function
        songTime()

        # configure slider
        songSlider.config(to=songLength, value=0)

    # adding frame for player controls
    controlsFrame = Frame(window)

    # packing frame at the bottom
    controlsFrame.pack(side=BOTTOM, padx=4, pady=4)

    # creating buttons
    previousImage = PhotoImage(file='previous.png')
    previousButton = Button(controlsFrame,
                            image=previousImage,
                            command=previousSong,
                            borderwidth=0,
                            relief=FLAT)
    previousButton.grid(row=0, column=0, padx=12, pady=8)

    pauseImage = PhotoImage(file='pause.png')
    pauseButton = Button(controlsFrame,
                         image=pauseImage,
                         command=pause,
                         borderwidth=0,
                         relief=FLAT)
    pauseButton.grid(row=0, column=1, padx=12, pady=8)

    playImage = PhotoImage(file='play.png')
    playButton = Button(controlsFrame,
                        image=playImage,
                        command=play,
                        borderwidth=0,
                        relief=FLAT)
    playButton.grid(row=0, column=2, padx=12, pady=8)

    stopImage = PhotoImage(file='stop.png')
    stopButton = Button(controlsFrame,
                        image=stopImage,
                        command=stop,
                        borderwidth=0,
                        relief=FLAT)
    stopButton.grid(row=0, column=3, padx=12, pady=8)

    nextImage = PhotoImage(file='next.png')
    nextButton = Button(controlsFrame,
                        image=nextImage,
                        command=nextSong,
                        borderwidth=0,
                        relief=FLAT)
    nextButton.grid(row=0, column=4, padx=12, pady=8)

    # function to change volume
    def changeVolume(value):
        pygame.mixer.music.set_volume(float(value) / 100)

    # creating volume label
    muteImage = PhotoImage(file='mute.png')
    volumeLabel = Label(controlsFrame,
                        image=muteImage,
                        borderwidth=0,
                        relief=FLAT)
    volumeLabel.grid(row=1, column=0, pady=10)

    fullVolumeImage = PhotoImage(file='fullVolume.png')
    volumeLabel = Label(controlsFrame,
                        image=fullVolumeImage,
                        borderwidth=0,
                        relief=FLAT)
    volumeLabel.grid(row=1, column=4, pady=10)

    # creating scale for volume control
    volumeScale = Scale(controlsFrame,
                        from_=0,
                        to=100,
                        orient=HORIZONTAL,
                        command=changeVolume,
                        relief=FLAT,
                        borderwidth=1,
                        width=12,
                        length=250,
                        font=('Inter', 10),
                        sliderlength=15,
                        sliderrelief=FLAT)
    volumeScale.set(50)
    volumeScale.grid(row=1, column=1, columnspan=3, pady=15)

    # calling mainloop function to run the application
    window.mainloop()


# main driver function
def main():
    MusicPlayer()


# main function call
if __name__ == '__main__':
    main()
