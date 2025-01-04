import tkinter as tk
from PIL import Image, ImageTk
import pygame
import requests
from io import BytesIO
import datetime

# Initialize Pygame for music
pygame.mixer.init()

# Function to play music
def play_music():
    pygame.mixer.music.load(r"C:\Users\marvx\Downloads\Interstellar Main Theme - Extra Extended - Soundtrack by Hans Zimmer.mp3")
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

api_key_nasa = "6uUOEbJFRheh4RFOH51513CBe1dw4Rbcsy7qlFvn"
base_url_nasa = "https://api.nasa.gov/planetary/apod"
params_nasa = {'api_key': api_key_nasa}

def load_new_data(image_label, title_label, explanation_label):
    response = requests.get(base_url_nasa, params=params_nasa)
    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "No title available")
        explanation = data.get("explanation", "No explanation available.")
        image_url = data.get("url", "")
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            img_tk = ImageTk.PhotoImage(image)
            image_label.configure(image=img_tk)
            image_label.image = img_tk

        title_label.configure(text=title)
        explanation_label.configure(text=explanation)

def fetch_history():
    url = "https://www.mediawiki.org/w/api.php"
    params = {
        "format": "json",
        "action": "query",
        "prop": "extracts",
        "titles": "On_this_day/January_4",
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        page = data["query"]["pages"][0]
        history_fact = page["extract"]
    except KeyError:
        history_fact = "No historical events recorded for today."
    
    return history_fact

def show_history(history_label):
    history_fact = fetch_history()
    history_label.configure(text=history_fact)

def is_new_day(last_updated_date):
    current_date = datetime.date.today()
    return current_date != last_updated_date

last_updated_date = datetime.date.today()

def refresh_data(image_label, title_label, explanation_label, history_label):
    global last_updated_date
    if is_new_day(last_updated_date):
        load_new_data(image_label, title_label, explanation_label)
        show_history(history_label)
        last_updated_date = datetime.date.today()

root = tk.Tk()
root.title("Space Facts and Music Viewer")

bg_image = Image.open(r"C:\Users\marvx\Downloads\tumblr_ngj74x9GsL1toa8s4o1_500.gif")  # Starry background image
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to match window size
bg_img_tk = tk.PhotoImage(file=r"C:\Users\marvx\Downloads\tumblr_ngj74x9GsL1toa8s4o1_500.gif")
bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

logo_image = Image.open(r"C:\Users\marvx\Downloads\Moon_rotating_full_220px.gif").convert("RGBA")  # Moon logo image
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resize the logo
logo_img_tk = tk.PhotoImage(file=r"C:\Users\marvx\Downloads\Moon_rotating_full_220px.gif")
logo_label = tk.Label(root, image=logo_img_tk)
logo_label.pack(pady=10)  # Display the logo at the top

def create_apod_window():
    apod_window = tk.Toplevel(root)
    apod_window.title("NASA Astronomy Picture of the Day")
    
    image_label = tk.Label(apod_window)
    image_label.pack()

    title_label = tk.Label(apod_window, text="", font=("Orbitron", 16, "bold"))
    title_label.pack(pady=10)

    explanation_label = tk.Label(apod_window, text="", wraplength=800, font=("Orbitron", 12), justify="left")
    explanation_label.pack(pady=10)

    load_button = tk.Button(apod_window, text="Load New APOD", command=lambda: load_new_data(image_label, title_label, explanation_label))
    load_button.pack(pady=20)

    apod_window.mainloop()

def create_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("This Day in Space History")

    history_label = tk.Label(history_window, text="", wraplength=800, font=("Orbitron", 12), justify="left")
    history_label.pack(pady=10)

    history_button = tk.Button(history_window, text="Fetch History", command=lambda: show_history(history_label))
    history_button.pack(pady=10)

    history_window.mainloop()

apod_button = tk.Button(root, text="NASA APOD", font=("Orbitron", 12), command=create_apod_window)
apod_button.pack(pady=10)

history_button = tk.Button(root, text="This Day in Space History", font=("Orbitron", 12), command=create_history_window)
history_button.pack(pady=10)

music_button = tk.Button(root, text="Play Interstellar Theme", font=("Orbitron", 12), command=play_music)
music_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Music", font=("Orbitron", 12), command=stop_music)
stop_button.pack(pady=10)

image_label = tk.Label(root)
title_label = tk.Label(root, text="", font=("Orbitron", 12))
explanation_label = tk.Label(root, text="", font=("Orbitron", 12), justify="left")
history_label = tk.Label(root, text="", font=("Orbitron", 12), justify="left")

refresh_data(image_label, title_label, explanation_label, history_label)

root.mainloop()
