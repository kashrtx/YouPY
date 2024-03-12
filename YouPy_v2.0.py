# Credit to Parth Jadhav for Tkinker-Designer module
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import re
from bs4 import BeautifulSoup
from pytube import YouTube, Playlist
import threading
import requests
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("814x730")
window.title("YouPY: MP4 & MP3 Converter")
window.configure(bg="#FFFFFF")

# Bool Selection for validating between .mp3 and .mp4 conversions
selected_mp3 = False
selected_mp4 = False

# Check if button_4 is clicked (file selector).
button_4_clicked = False

# Save file path globally.
save_file_path_var = ''

# Global valid url check variable.
valid_yt_url = False

# store video title name
yt_video_title = ''
yt_filename = ''

# Create Canvas
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=730,
    width=814,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    819.0,
    730.0,
    fill="#000000",
    outline="")

canvas.create_text(
    303.0,
    151.0,
    anchor="nw",
    text="Enter The YT URL",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 24 * -1, 'bold')
)

canvas.create_text(
    9.0,
    294.0,
    anchor="nw",
    text="Select Conversion Type (mp4 or mp3): ",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 24 * -1, 'bold')
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    410.5,
    222.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#B8A8A8",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=35.0,
    y=196.0,
    width=751.0,
    height=50.0
)
# Url variable

# The status message for the program.
ready_text = canvas.create_text(
    9.0,
    689.0,
    anchor="nw",
    text="Ready For Conversion",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 24 * -1, 'bold')
)

# The convert button that is the heart of the code.
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: conversion_logic(entry_1.get().strip()),
    relief="flat"
)
button_1.place(
    x=158.0,
    y=524.0,
    width=512.0,
    height=135.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    409.0,
    53.0,
    image=image_image_1
)

# MP4 Conversion Type Button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: select_mp4_conversion(),
    relief="flat"
)
button_2.place(
    x=9.0,
    y=342.0,
    width=120.0,
    height=124.0
)

# MP3 Conversion Type Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: select_mp3_conversion(),
    relief="flat"
)
button_3.place(
    x=332.0,
    y=342.0,
    width=120.0,
    height=124.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_file_selector(),
    relief="flat"
)
button_4.place(
    x=537.0,
    y=286.0,
    width=282.0,
    height=229.0
)


def open_file_selector():
    """
    This function prompts user to select a folder to save, and puts that
    file path in a global variable called save_file_path_var to be
    accessed throughout the program.

    :return: str
    """
    print("button_4 clicked")
    # Define global variables
    global button_4_clicked
    global save_file_path_var
    try:
        # Ask to prompt save file location
        file_path = filedialog.askdirectory()
        # Get file location folder name
        file_location = file_path.split('/')[-1]

        # save that file path into a global variable named save_file_path
        save_file_path_var = file_path + '/'

        # Check for valid file location in order to enable receive button.
        if save_file_path_var:
            button_4_clicked = True
        else:
            button_4_clicked = False

        # Output status
        canvas.itemconfig(ready_text, text=f"Saving To: {file_location} Folder")
        print(save_file_path_var)
        return save_file_path_var
    except Exception as e:
        print(e)
        canvas.itemconfig(ready_text, text=f"Error Saving File: {e}")


def select_mp3_conversion():
    """
    This function selects the mp4 conversion when the button is pressed.

    :return:
    """
    global selected_mp3
    global selected_mp4
    selected_mp3 = True
    selected_mp4 = False
    print(f"MP4: {selected_mp4}, MP3: {selected_mp3}")
    canvas.itemconfig(ready_text, text="MP3 Conversion Selected")


def select_mp4_conversion():
    """
    This function selects the mp4 conversion when the button is pressed.

    :return:
    """
    global selected_mp3
    global selected_mp4
    selected_mp3 = False
    selected_mp4 = True
    print(f"MP4: {selected_mp4}, MP3: {selected_mp3}")
    canvas.itemconfig(ready_text, text="MP4 Conversion Selected")


def get_video_title(url):
    """
    This function gets the title of the YouTube video from URL.

    :return: str
    """
    global yt_video_title
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').string
    return title[:-10]


def check_valid_url(url):
    """
    This function checks if the URL is valid and it's from YouTube.

    :return:
    """
    try:
        global valid_yt_url
        global yt_video_title
        global yt_filename
        r = requests.get(url)
        site = 'youtube.com'
        shortcut = 'youtu.be'
        if "Video unavailable" not in r.text and (site in url or shortcut):
            # Check if the URL is a playlist
            if any(x in url for x in ['list', 'playlist']):
                valid_yt_url = True
                yt_video_title = "Playlist"
                yt_filename = "Playlist"
            else:
                # Get the YT Video Title and store it in yt_video_title variable.
                yt_video_title = get_video_title(url)

                # Format the YT video title and make it into a valid file name.
                yt_filename = yt_filename_fix(yt_video_title)

                # Output video title name
                print(f'YouTube Video Selected: {yt_video_title}')
                canvas.itemconfig(ready_text, text=f'{yt_video_title}')

                # Change global variable to validate url.
                valid_yt_url = True
        else:
            valid_yt_url = False
    except Exception as e:
        print(e)


def yt_filename_fix(title):
    """
    Optional: Makes a valid file name format according to windows
    requirements. The YT Video Title gets formatted from regex.

    :return: str
    """
    regex = re.compile(r'[\\/:*?"<>|]')
    return str(regex.sub('', title))


def show_progress_bar(stream, chunk, bytes_remaining):
    """
    This function Show a progress bar when downloading
    either an mp4 or mp3 after the validations are
    complete.

    :return:
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(f"{percentage_of_completion:.2f}% downloaded")
    canvas.itemconfig(ready_text,
                      text=f"{percentage_of_completion:.2f}% Downloaded")


def convert_to_mp3(yt_url):
    """
    Get the url from the the input box and then convert the youtube video to
    mp3 format when function is called.
    :param yt_url:
    :return:
    """
    print('Now converting to MP3\n')
    print("Because of updates to YouTube, you must authorize your device to use"
          " this app. Instructions below in console (ignore if this step has "
          "been already done):\n")
    yt = YouTube(yt_url, on_progress_callback=show_progress_bar, use_oauth=True,
                 allow_oauth_cache=True)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path=save_file_path_var,
                    filename=f"{yt_filename}.mp3")
    print(f"Completed Download: {yt_video_title}")
    canvas.itemconfig(ready_text, text=f"Download Complete:"
                                       f" {yt_video_title}")


def convert_to_mp4(yt_url):
    """
    Get the url from the the input box and then convert the youtube video to
    mp4 format when function is called.
    :param yt_url:
    :return:
    """
    print('Now converting to MP4\n')
    print("Because of updates to YouTube, you must authorize your device to use"
          " this app. Instructions below in console (ignore if this step has "
          "been already done):\n")
    yt = YouTube(yt_url, on_progress_callback=show_progress_bar, use_oauth=True,
                 allow_oauth_cache=True)
    stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
    stream.download(output_path=save_file_path_var)
    print(f"Completed Download: {yt_video_title}")
    canvas.itemconfig(ready_text, text=f"Download Complete:"
                                       f" {yt_video_title}")


def conversion_logic(yt_url):
    """
    The core function that handles the conversion process. It checks
    whether the entered URL is a valid YouTube URL (valid_yt_url bool
    global variable) and whether a  file path (button_4 clicked?)
    has been selected.If the input is valid (conversion method selected
    to be mp3 or mp4),it begins the download process and starts a thread
    to update the status message on the canvas. Once the download is
    complete, it uses the pytube module to convert the file to the
    selected format and save it to the selected file path. The status
    message is then updated to indicate that the conversion is complete.

    :return:
    """
    print('button 1 clicked')
    global button_4_clicked

    # start threading for check_valid_url function to prevent freezing
    # Does request for valid youtube url check.
    start_url_thread = threading.Thread(target=check_valid_url(yt_url))
    start_url_thread.start()

    # Check if url is a valid YouTube URL

    if valid_yt_url and button_4_clicked:
        def start_conversion_thread():
            """
                This function serves a thread to prevent freezing and runs
                when there is a file save location selected.

                :return:
                """
            # create a file path variable with the file name in it.
            # file_path_with_name = f'{save_file_path_var}{yt_filename}'
            # print(file_path_with_name)
            # Do mp3 conversion
            try:
                if selected_mp3:
                    # Check if the URL is a playlist
                    if yt_video_title == "Playlist":
                        playlist = Playlist(yt_url)
                        total_videos = len(playlist.videos)
                        current_video = 1
                        for video in playlist.videos:
                            canvas.itemconfig(ready_text, text=f"Downloading Playlist: ({current_video}:{video.title}/{total_videos})")
                            video.streams.filter(only_audio=True, mime_type='audio/mp4').first().download(output_path=save_file_path_var, 
                                                                                                          filename=f"{video.title}.mp3")
                            current_video += 1
                        canvas.itemconfig(ready_text, text=f"Finished Downloading Playlist!")
                    else:
                        convert_to_mp3(yt_url)

                # Do mp4 conversion
                elif selected_mp4:
                    # Check if the URL is a playlist
                    if yt_video_title == "Playlist":
                        playlist = Playlist(yt_url)
                        total_videos = len(playlist.videos)
                        current_video = 1
                        for video in playlist.videos:
                            canvas.itemconfig(ready_text, text=f"Downloading Playlist: ({current_video}:{video.title}/{total_videos})")
                            video.streams.filter(file_extension='mp4').get_highest_resolution().download(output_path=save_file_path_var)
                            current_video += 1
                        canvas.itemconfig(ready_text, text=f"Finished Downloading Playlist!")
                    else:
                        convert_to_mp4(yt_url)

                # Otherwise No conversion type option was selected
                else:
                    print('No Conversion Method Selected!')
                    canvas.itemconfig(ready_text,
                                      text="Please Select A Conversion "
                                           "Method!")
            # Catch any errors
            except Exception as e:
                print(e)
                canvas.itemconfig(ready_text,
                                  text=f"{e}")

        # Start the conversion thread
        start_conversion_thread = threading.Thread(
            target=start_conversion_thread)
        start_conversion_thread.start()

    # Invalid URL error
    elif not valid_yt_url:
        print('Invalid URL! Please Insert YouTube Video URL!')
        canvas.itemconfig(ready_text, text="Invalid URL! Please Insert YouTube "
                                           "Video URL!")

    # No file save location detected
    else:
        print('No file save location')
        canvas.itemconfig(ready_text,
                          text="No file save location selected!")


# End of program
window.resizable(False, False)
window.mainloop()
