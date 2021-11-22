# Python Music Player
#-----------------------------------------------------------------------------------------IMPORTING ALL REQUIRED MODULES AND LIBARIES----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()     #------------------------------------------------------------------> (main frame--> root)
root.title("Mp3 Player")
root.iconbitmap(r'music player logo.ico')
root.geometry("540x380")   # 540x380
# root.configure(background='white')     # for changing the bg color of the whole window except the playlist box window
# initialize pygame mixer
pygame.mixer.init()


# -----------------------------------------------------------------------MENU BAR FUNCTIONLALITY------------------------------------------------------------------------------------------------------------------------
# "open" function (only can select one song)
def Open():
    song = filedialog.askopenfilename(initialdir='F:\Music\song(trail for music player)', title= "Choose a song", filetypes= (("mp3 Files","*mp3"),))

    # strip away the path of the song and just print the song name in the playlist
    song = song.replace("F:/Music/song(trail for music player)/","")
    song = song.replace(".mp3", "")
    playlist_box.insert(END, song)
# "Add song" function (can select one as well as more than one song

def add_song():
    songs = filedialog.askopenfilenames(initialdir='F:\Music\song(trail for music player)', title="Choose your songs",
                                        filetypes=(("mp3 Files", "*mp3"),))

    for song in songs:
        # strip away the path of the song and just print the song name in the playlist
        song = song.replace("F:/Music/song(trail for music player)/", "")
        song = song.replace(".mp3", "")

        # for inserting the song to the playlist
        playlist_box.insert(END, song)


# exit the window trough exit menu option
def Exit():
    root.destroy()
    exit()





# --------------------------------------------------------------------------PLAYING FUNCTIONALITY OF THE MUSIC PLAYER----------------------------------------------------------------------------
#lenght of the song
def play_time():
    if stopped:
        return
    # time elapsed by the current song (in milli second) then converted to second by dividing it by 1000
    Current_Time = pygame.mixer.music.get_pos() / 1000

    # (for rough- better understanding or checking if the slider position and the song position is synced properly or not)
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song pos: {int(Current_Time)}')

    # convert it into time format
    global converted_Current_Time
    converted_Current_Time = time.strftime('%M:%S', time.gmtime(Current_Time))


    # get the active/currently playing song
    #current_song = playlist_box.curselection()

    song = playlist_box.get(ACTIVE)
    # add the directory/path of the song title
    song = f'F:/Music/song(trail for music player)/{song}.mp3'
    song_mut= MP3(song)
    # get song length with mutagen
    global song_lenght
    song_lenght = song_mut.info.length

    # convert to time format
    converted_Song_Lenght = time.strftime('%M:%S', time.gmtime(song_lenght))

    #increse current time by one so that it can be synced well with the song's current position
    Current_Time += 1

    if int(my_slider.get()) == int(song_lenght):
        status_bar.config(text=f'Time Elapsed: {converted_Song_Lenght} of  {converted_Song_Lenght}    ')

    elif paused:
        pass

    elif int(my_slider.get()) == int(Current_Time):
        # slider hasn't been moved
        slider_position = int(song_lenght)
        my_slider.config(to=slider_position, value=int(Current_Time))

    else:
        # slider has been moved!
        slider_position = int(song_lenght)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_Current_Time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_Current_Time} of  {converted_Song_Lenght}    ')

        # move the song length from where the slider positioned by the mouse
        next_time = int(my_slider.get()) + 1
        my_slider.config(value= next_time)

    # output shown in the status bar in integer format
    # status_bar.config(text=f'Time Elapsed: {converted_Current_Time} of  {converted_Song_Lenght}    ')
    #update slider position as of current running/ active song
    #my_slider.config(value=int(Current_Time))
    # this shows us the time in incresing form as the song starts the time also increases
    status_bar.after(1000, play_time)  # this very imp bcoz this is reason of the increasing of the current song duration (& this is not inside the if block rather its inside the def block



# -----------------------------------------------------------------FUNCTIONALITY OF THE BUTTONS--------------------------------------------------------------------------------------------------------------------------------------
# delete a single song from the playlist
def delete_song():
    stop()
    playlist_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# delete all the songs from the playlist
def delete_all_song():
    stop()
    playlist_box.delete(0, END)
    pygame.mixer.music.stop()


# play selected song
def play():
    global stopped
    stopped = False
    song = playlist_box.get(ACTIVE)
    song = f'F:/Music/song(trail for music player)/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # call the play_time function to see the lenght of the song
    play_time()
    # update slider to position
    slider_position = int(song_lenght)
    my_slider.config(to= slider_position, value=0)


# set a stopped variable globally (outside)
global stopped
stopped = False


# stop song
def stop():
    # Reset status bar when a song is stopped
    status_bar.config(text='')
    my_slider.config(value=0)
    # stop the song from playing
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)

    # calling and clearing the status bar
    status_bar.config(text='Song is Stopped - Play It Again ')

    # set a stopped variable globally (inside)
    global stopped
    stopped = True



# create global pause variable
global paused
paused = False


# pause and unpause a song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # then unpause it
        pygame.mixer.music.unpause()
        paused = False  # if its playing then it will pass false(indicating that its not paused) and the paused valu will be false and it will pause the song
    else:
        # if its paused then pass true so that it will go to the above and unpause it
        pygame.mixer.music.pause()
        paused = True


# play the  next song functionality
def next_song():
    # Reset status bar when a song is stopped
    status_bar.config(text='')
    my_slider.config(value=0)
    # get the current song's tuple number
    next_one = playlist_box.curselection()  # this will return the no of the song in the playlist in the form of tuple
    # to go to the next song we have to add 1 to the playlist(where items are in tuple form) and it will play the next song
    next_one = next_one[0] + 1
    # get the next song from the playlist
    song = playlist_box.get(next_one)
    # add the directory of the song title
    song = f'F:/Music/song(trail for music player)/{song}.mp3'
    # now load and play the next song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear the prev active bar from the previous song
    playlist_box.selection_clear(0, END)
    # change the active song bar to the next song currently playing
    playlist_box.activate(next_one)
    # set the active bar to the next currently playing song
    playlist_box.selection_set(next_one, last=None)


# play the previous song
def prev():
    # Reset status bar when a song is stopped
    status_bar.config(text='')
    my_slider.config(value=0)
    # get the current song's tuple number
    prev_one = playlist_box.curselection()  # this will return the no of the song in the playlist in the form of tuple
    # to go to the next song we have to add 1 to the playlist(where items are in tuple form) and it will play the next song
    prev_one = prev_one[0] - 1
    # get the prev song from the playlist
    song = playlist_box.get(prev_one)
    # add the directory of the song title
    song = f'F:/Music/song(trail for music player)/{song}.mp3'
    # now load and play the previous song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear the next song's active bar from the next song
    playlist_box.selection_clear(0, END)
    # change the active song bar to the prev song currently playing
    playlist_box.activate(prev_one)
    # set the active bar to the prev currently playing song
    playlist_box.selection_set(prev_one, last=None)

# create a function for volume
def volume(X):
    pygame.mixer.music.set_volume(vol_slider.get())
    # volume = int(val)/100
    # pygame.mixer.music.set_volume(volume)

# create mute and unmute functionality
global muted  # declare a mutted variable for future use
muted = False
def mute():
    global muted

    if muted:  # if muted = true then unmute the volume button
        pygame.mixer.music.set_volume(1)
        volume_button.configure(image=volume_Img)
        vol_slider.set(1)
        muted = False
    else:      # if muted  = false then show the umute button as well as turn the volume to zero
        pygame.mixer.music.set_volume(0)
        volume_button.configure(image=mute_Img)
        vol_slider.set(0)
        muted = True
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------SLIDER FUNCTIONALITY-----------------------------------------------------------------------------------------------------------------

# slider function
def slider(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_lenght)}')
    song = playlist_box.get(ACTIVE)
    song = f'F:/Music/song(trail for music player)/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start= int(my_slider.get()))

#-----------------------------------------------------------------CREATION OF DIFFERENT FRAMES-----------------------------------------------------------------------------------------------------------------

# 1. create master frame for volume control and also for playlist box-------------------------------------------------------------------> (frame to create playlist frame)
master_frame = Frame(root)
master_frame.pack(pady= 10)

# 2. create player control frame (where the buttons will be present)---------------------------------------------------------------------> (frame for the buttons)
controls_frame = Frame(master_frame)  # we changed it from root to master_frame bcoz we want our buttons will be present over there
controls_frame.grid(row=1, column=0, pady=20)

# 3.1. create a volume frame---------------------------------------------------------------------------------------------------------------> (frame for the volume)
volume_frame = LabelFrame(master_frame, text= 'Volume') #
volume_frame.grid(row=0, column=1, padx=10)   #

# 3.2. create a frame where mute and unmute button will be shown----------------------------------------------------------------------------> (another frame for the mute and unmute inside the volume frame )
mute_frame = Frame(master_frame)  # we changed it from root to master_frame bcoz we want our buttons will be present over there
mute_frame.grid(row=1, column=1, pady=2)


# 4. create playlist box---------------------------------------------------------------------------------------------------------------------> (frame for the playlist box)
playlist_box = Listbox(master_frame, bg="white", fg="black", width=70)  # change the bg color of the playlist box frame
playlist_box.grid(row=0, column=0)   # pady=20 not required as we alredy given pady=20 in the master frame, so it will do the job

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------CREATING AND DEFING THE BUTTONS----------------------------------------------------------------------------------------------------------------------

# Define player control buttons
play_Img = PhotoImage(file='play.png')
pause_Img = PhotoImage(file='pause.png')
prev_Img = PhotoImage(file='prev.png')
next1_Img = PhotoImage(file='next.png')
stop_Img = PhotoImage(file='stop.png')
mute_Img = PhotoImage(file='mute.png')
volume_Img = PhotoImage(file='unmute.png')



# create the buttons on the screen
play_button = ttk.Button(controls_frame, image=play_Img, command=play)                                        # , borderwidth=0
pause_button = ttk.Button(controls_frame, image=pause_Img, command=lambda: pause(paused))                     # , borderwidth=0
stop_button = ttk.Button(controls_frame, image=stop_Img, command=stop)                                        # , borderwidth=0
prev_button = ttk.Button(controls_frame, image=prev_Img, command=prev)                                        # , borderwidth=0
next1_button = ttk.Button(controls_frame, image=next1_Img, command=next_song)                                 # , borderwidth=0
volume_button =  ttk.Button(mute_frame, image=volume_Img, command=mute)



# putting all the buttons in same row and diff column
play_button.grid(row=0, column=0, padx=5)
pause_button.grid(row=0, column=1, padx=5)
stop_button.grid(row=0, column=2, padx=5)
prev_button.grid(row=0, column=3, padx=5)
next1_button.grid(row=0, column=4, padx=5)
volume_button.grid(row=0, column=5, padx=20)  #

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------MENU BAR-------------------------------------------------------------------------------------------------------------------------------------------
# create menu
my_menu = Menu(root)
root.config(menu=my_menu)  # so that the menu bar should in the top

# Add menus such as ("File"), ("playlist"--->"Add song", "Delete songs"),  ("Help")

# 1. menu options for file and help
file = Menu(my_menu, tearoff=0)  # "tearoff= 0" is used to remove the underscore happening inside our dropdown option
Help = Menu(my_menu, tearoff=0)  # "tearoff= 0" is used to remove the underscore happening inside our dropdown option
# file dropdown menus
my_menu.add_cascade(label="File", menu=file)
file.add_command(label="Open", command=Open)
file.add_command(label="Exit", command=Exit)

## 2. playlist
add_song_menu = Menu(my_menu,tearoff=0)  # "tearoff= 0" is used to remove the underscore happening inside our dropdown option
my_menu.add_cascade(label="PLayList", menu=add_song_menu)
# add song
add_song_menu.add_command(label="Add songs", command=add_song)
# delete a song
add_song_menu.add_command(label="Delete a song", command=delete_song)
# delete all songs at once
add_song_menu.add_command(label="Delete all songs", command=delete_all_song)

# 3. help drop down menu
my_menu.add_cascade(label="Help", menu=Help)
Help.add_command(label="Help !!")
Help.add_command(label="Check for updates --")
# Help.add_command(label="About")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------STATUS BAR--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# create status bar
status_bar = Label(root, text='Welcome to MP3 Player', bd=1, relief=GROOVE, anchor=E, font= 'Times 10 italic')
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------SLIDER FOR SONG AND VOLUME--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# music positional slider for our music player
my_slider = ttk.Scale(master_frame ,from_=0, to=100, orient= HORIZONTAL, value=0, command= slider, length= 340)
my_slider.grid(row=2, column=0, pady= 10)

# volume slider
vol_slider =  ttk.Scale(volume_frame, from_=0, to=1, orient= VERTICAL, value=1, command= volume, length= 125)
#vol_slider.set(70)
vol_slider.pack(pady= 10)    # row=0, column=1 can not be used inside a pack function, those can only be used inside a grid function

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

root.mainloop()
