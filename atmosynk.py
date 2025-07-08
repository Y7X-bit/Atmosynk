import customtkinter as ctk
import requests, datetime, os, threading
import speech_recognition as sr

# 💠 Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 🎤 Speak using macOS 'say' in a thread
def speak(text):
    def run_say():
        os.system(f'say "{text}"')
    threading.Thread(target=run_say).start()

# 📍 Get city from IP
def get_location():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        return res.get("city", "Delhi")
    except:
        return "Delhi"

# ☁️ Get weather from wttr.in
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

# 🌈 Weather to emoji
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

# 🔁 Search + Speak
def search_weather(city=None):
    if not city:
        city = city_entry.get()
    if not city:
        city = get_location()

    weather = fetch_weather(city)
    icon = emoji_for(weather)
    result = f"{icon} Weather in {city.title()}: {weather}"
    result_label.configure(text=result)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"{timestamp} — {result}")
    speak(result)

# 💾 Save to .txt
def save_to_file():
    with open("weather_history.txt", "w") as f:
        f.write("\n".join(history))
    result_label.configure(text="✅ History saved!")
    speak("Weather history saved!")

# 🎙️ Voice input
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

# 📴 Silent first-time load (NO voice)
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
app.title("🌤️ Weather Pro Max — Y7X")
app.geometry("520x500")
app.minsize(500, 460)

history = []

frame = ctk.CTkFrame(master=app, corner_radius=20)
frame.pack(padx=20, pady=20, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="🌍 Real-Time Weather", font=("Helvetica Neue", 24, "bold"))
title.pack(pady=(15, 10))

city_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter city or leave blank for auto-location")
city_entry.pack(pady=10, ipady=6, ipadx=10)

btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="📍 Auto Detect", command=lambda: search_weather(get_location()), width=140).pack(side="left", padx=5)
ctk.CTkButton(btn_frame, text="🎤 Voice Input", command=voice_input, width=140).pack(side="left", padx=5)

ctk.CTkButton(master=frame, text="🔁 Refresh / Search", command=search_weather, width=300).pack(pady=5)
ctk.CTkButton(master=frame, text="💾 Save to File", command=save_to_file, width=300).pack(pady=5)

result_label = ctk.CTkLabel(master=frame, text="", font=("SF Pro", 18), wraplength=440, justify="center")
result_label.pack(pady=20)

footer = ctk.CTkLabel(app, text="🔎 Powered by Y7X 💗", font=("SF Pro", 14))
footer.pack(pady=10)

# Load weather silently at startup ✅
silent_initial_weather()

app.mainloop()