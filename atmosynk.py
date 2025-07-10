import customtkinter as ctk
import requests, datetime, os, threading
import speech_recognition as sr

# 💠 Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def speak(text):
    def run_say():
        os.system(f'say "{text}"')
    threading.Thread(target=run_say).start()

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("city", "Delhi")
    except:
        return "Delhi"

def fetch_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return "Weather unavailable"
    except:
        return "Error fetching weather"

def emoji_for(weather):
    weather = weather.lower()
    if "sun" in weather:
        return "☀️"
    elif "rain" in weather:
        return "🌧️"
    elif "cloud" in weather:
        return "☁️"
    elif "storm" in weather:
        return "⛈️"
    elif "snow" in weather:
        return "❄️"
    elif "fog" in weather or "mist" in weather:
        return "🌫️"
    else:
        return "🌤️"

def search_weather(city=None):
    if not city:
        city = city_entry.get()
    if not city:
        city = get_location()
        city_entry.delete(0, ctk.END)
        city_entry.insert(0, city)

    weather = fetch_weather(city)
    icon = emoji_for(weather)
    result = f"{icon} Weather in {city.title()}: {weather}"
    result_label.configure(text=result)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"{timestamp} — {result}")
    speak(result)

def save_to_file():
    with open("weather_history.txt", "w") as f:
        f.write("\n".join(history))
    result_label.configure(text="✅ History saved!")
    speak("Weather history saved!")

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say the city name now")
        try:
            audio = recognizer.listen(source, timeout=5)
            city = recognizer.recognize_google(audio)
            city_entry.delete(0, ctk.END)
            city_entry.insert(0, city)
            search_weather(city)
        except:
            speak("Sorry, I couldn't understand.")

def silent_initial_weather():
    city = get_location()
    weather = fetch_weather(city)
    icon = emoji_for(weather)
    result = f"{icon} Weather in {city.title()}: {weather}"
    result_label.configure(text=result)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"{timestamp} — {result}")

# ---------------- GUI ----------------

app = ctk.CTk()
app.title("🌤️ Atmosynk — Powered by Y7X")
app.geometry("550x520")
app.configure(fg_color="#000000")  # AMOLED black

history = []

frame = ctk.CTkFrame(master=app, corner_radius=20, fg_color="#0a0a0a", border_color="#ff0000", border_width=2)
frame.pack(padx=20, pady=20, fill="both", expand=True)

title = ctk.CTkLabel(
    master=frame,
    text="🌍 ATMOSYNK",
    font=("SF Pro Display", 28, "bold"),
    text_color="#ff0000"
)
title.pack(pady=(15, 10))

city_entry = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter city or leave blank for auto-location",
    width=400,
    height=40,
    border_color="#ff0000",
    border_width=2,
    corner_radius=15,
    text_color="#ffffff",
    fg_color="#121212"
)
city_entry.pack(pady=10)

btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
btn_frame.pack(pady=10)

def red_button(text, command, w=140):
    return ctk.CTkButton(
        btn_frame,
        text=text,
        command=command,
        width=w,
        height=38,
        border_color="#ff0000",
        border_width=2,
        fg_color="#000000",
        text_color="#ff0000",
        hover_color="#1a1a1a",
        corner_radius=20,
    )

red_button("📍 Auto Detect", lambda: search_weather(get_location())).pack(side="left", padx=5)
red_button("🎤 Voice Input", voice_input).pack(side="left", padx=5)

ctk.CTkButton(
    master=frame,
    text="🔁 Refresh / Search",
    command=search_weather,
    width=300,
    height=40,
    border_color="#ff0000",
    border_width=2,
    fg_color="#000000",
    text_color="#ff0000",
    hover_color="#1a1a1a",
    corner_radius=20,
).pack(pady=5)

ctk.CTkButton(
    master=frame,
    text="💾 Save to File",
    command=save_to_file,
    width=300,
    height=40,
    border_color="#ff0000",
    border_width=2,
    fg_color="#000000",
    text_color="#ff0000",
    hover_color="#1a1a1a",
    corner_radius=20,
).pack(pady=5)

result_label = ctk.CTkLabel(
    master=frame,
    text="",
    font=("SF Pro", 18),
    text_color="#ffffff",
    wraplength=440,
    justify="center"
)
result_label.pack(pady=20)

footer = ctk.CTkLabel(
    app,
    text="🔎 Powered by Y7X 💗",
    font=("SF Pro", 14),
    text_color="#ff0000"
)
footer.pack(pady=10)

# 📴 No auto voice on startup
silent_initial_weather()

app.mainloop()