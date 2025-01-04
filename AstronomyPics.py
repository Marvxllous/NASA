import tkinter as tk
from PIL import Image, ImageTk
import time
import requests
from io import BytesIO
import pygame
import random

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
            image = image.resize((800, 600), Image.Resampling.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)
            image_label.config(image=image_tk)
            image_label.image = image_tk  # Keep a reference to avoid garbage collection
            title_label.config(text=title)
            explanation_label.config(text=explanation)

def fetch_history():
    today = time.strftime("%B_%d")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "format": "json",
        "action": "query",
        "prop": "extracts",
        "titles": f"On_this_day/{today}",
        "explaintext": True,
        "exsectionformat": "plain",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data["query"]["pages"]
        for page_id in pages:
            extract = pages[page_id].get("extract", "No history available.")
            return extract
    return "Failed to fetch history."

def fetch_weather():
    api_key_weather = "your_openweather_api_key"
    base_url_weather = "http://api.openweathermap.org/data/2.5/weather"
    params_weather = {
        'q': 'New York',
        'appid': api_key_weather,
        'units': 'metric'
    }
    response = requests.get(base_url_weather, params=params_weather)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Weather: {weather}, Temperature: {temp}°C"
    return "Failed to fetch weather."

def fetch_quote():
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Quote of the Day: {data['content']} - {data['author']}"
    return "Failed to fetch quote."

def get_zodiac_sign():
    zodiac_signs = [
        ("Capricorn", (1, 1), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
        ("Capricorn", (12, 22), (12, 31))
    ]
    today = time.localtime()
    for sign, start, end in zodiac_signs:
        if (start <= (today.tm_mon, today.tm_mday) <= end):
            return f"Current Zodiac Sign: {sign}"
    return "Failed to determine zodiac sign."

def create_weather_window():
    weather_window = tk.Toplevel(root)
    weather_window.title("Current Weather")

    weather_text = fetch_weather()
    weather_label = tk.Label(weather_window, text=weather_text, wraplength=800, font=("Orbitron", 12), justify="left")
    weather_label.pack(pady=10)

def create_quote_window():
    quote_window = tk.Toplevel(root)
    quote_window.title("Quote of the Day")

    quote_text = fetch_quote()
    quote_label = tk.Label(quote_window, text=quote_text, wraplength=800, font=("Orbitron", 12), justify="left")
    quote_label.pack(pady=10)

def create_zodiac_window():
    zodiac_window = tk.Toplevel(root)
    zodiac_window.title("Current Zodiac Season")

    zodiac_text = get_zodiac_sign()
    zodiac_label = tk.Label(zodiac_window, text=zodiac_text, wraplength=800, font=("Orbitron", 12), justify="left")
    zodiac_label.pack(pady=10)

def show_random_fact():
    facts = [
        "Venus is the hottest planet in our solar system.",
        "A day on Venus is longer than a year on Venus.",
        "Jupiter has the shortest day of all the planets.",
        "The Sun contains 99.86% of the mass in the Solar System.",
        "Neutron stars can spin at a rate of 600 rotations per second."
    ]
    fact = random.choice(facts)
    fact_label.config(text=f"Random Space Fact: {fact}")

root = tk.Tk()
root.title("Space Facts and Music Viewer")

bg_image = Image.open(r"C:\Users\marvx\Downloads\tumblr_ngj74x9GsL1toa8s4o1_500.gif")  # Starry background image
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to match window size
bg_img_tk = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root)
bg_label.config(image=bg_img_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

logo_image = Image.open(r"C:\Users\marvx\Downloads\Moon_rotating_full_220px.gif").convert("RGBA")  # Moon logo image
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resize the logo
logo_img_tk = ImageTk.PhotoImage(logo_image)
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

    load_new_data(image_label, title_label, explanation_label)

def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

time_label = tk.Label(root, font=("Orbitron", 14), bg="black", fg="white")
time_label.pack(pady=10)
update_time()

apod_button = tk.Button(root, text="Show APOD", command=create_apod_window, font=("Orbitron", 14))
apod_button.pack(pady=10)

def create_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("On This Day in History")

    history_text = fetch_history()
    history_label = tk.Label(history_window, text=history_text, wraplength=800, font=("Orbitron", 12), justify="left")
    history_label.pack(pady=10)

history_button = tk.Button(root, text="On This Day", command=create_history_window, font=("Orbitron", 14))
history_button.pack(pady=10)

weather_button = tk.Button(root, text="Current Weather", command=create_weather_window, font=("Orbitron", 14))
weather_button.pack(pady=10)

quote_button = tk.Button(root, text="Quote of the Day", command=create_quote_window, font=("Orbitron", 14))
quote_button.pack(pady=10)

zodiac_button = tk.Button(root, text="Current Zodiac Season", command=create_zodiac_window, font=("Orbitron", 14))
zodiac_button.pack(pady=10)

fact_button = tk.Button(root, text="Random Space Fact", command=show_random_fact, font=("Orbitron", 14))
fact_button.pack(pady=10)

play_button = tk.Button(root, text="Play Music", command=play_music, font=("Orbitron", 14))
play_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Music", command=stop_music, font=("Orbitron", 14))
stop_button.pack(pady=10)

fact_label = tk.Label(root, font=("Orbitron", 14), bg="black", fg="white")
fact_label.pack(pady=10)

root.mainloop()
