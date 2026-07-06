import os
import webbrowser
import time
import json
from datetime import datetime
import speech_recognition as sr
from groq import Groq
import pyttsx3
from dotenv import load_dotenv
import requests

load_dotenv()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
recognizer = sr.Recognizer()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def speak(text):
    print(f"🎙️ JARVIS: {text}")
    try:
        print(f"  [DEBUG] About to speak: '{text}'")
        engine.say(text)
        print(f"  [DEBUG] Calling runAndWait()...")
        engine.runAndWait()
        print(f"  [DEBUG] Speaking complete")
    except Exception as e:
        print(f"  ❌ Speech error: {e}")
        import traceback
        traceback.print_exc()

def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # ← ADD THIS
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Microphone error: {e}")
        return None

def get_weather():
    """Get real weather from API"""
    try:
        # Free weather API (no key needed for basic use)
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=49.4&longitude=7.8&current=temperature_2m,weather_code"
        )
        data = response.json()
        temp = data['current']['temperature_2m']
        return f"The current temperature in Kaiserslautern is {temp}°C"
    except Exception as e:
        print(f"Weather error: {e}")
        return "I couldn't fetch the weather. Check weather.com"

def get_time():
    """Get real system time"""
    now = datetime.now().strftime("%I:%M %p")
    return f"It's currently {now}"

def get_date():
    """Get real system date"""
    today = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}"

def get_priorities():
    """Read priorities from jarvis_memory.json"""
    try:
        with open('jarvis_memory.json', 'r') as f:
            data = json.load(f)
            priorities = data.get('priorities', [])
            if priorities:
                priority_text = "Your priorities are: " + ", ".join(priorities[:3])
                return priority_text
            return "No priorities set"
    except Exception as e:
        print(f"Priority error: {e}")
        return "I couldn't read your priorities"

def get_emails():
    """Read emails from data.json"""
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            emails = data.get('emails', [])
            if emails:
                count = len(emails)
                latest = emails[0]['subject'] if emails else "unknown"
                return f"You have {count} unread emails. Latest: {latest}"
            return "No emails"
    except Exception as e:
        print(f"Email error: {e}")
        return "I couldn't read your emails"

def get_ai_response(user_input):
    """Handle queries dynamically"""
    user_lower = user_input.lower()
    
    # Weather
    if "weather" in user_lower or "temperature" in user_lower:
        return get_weather()
    
    # Time
    elif "time" in user_lower or "what time" in user_lower:
        return get_time()
    
    # Date
    elif "date" in user_lower or "today" in user_lower:
        return get_date()
    
    # Priorities
    elif "priority" in user_lower or "priorities" in user_lower:
        return get_priorities()
    
    # Emails
    elif "email" in user_lower or "gmail" in user_lower:
        return get_emails()
    
    # Help
    elif "help" in user_lower or "commands" in user_lower:
        return "Ask me about: weather, time, date, priorities, emails, or anything else!"
    
    # Default: Use Groq for general questions
    else:
        try:
            message = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=150,
                temperature=0.7
            )
            return message.choices[0].message.content
        except Exception as e:
            return "I'm thinking about that. Ask me again."

def main():
    print("Opening dashboard...")
    dashboard_path = os.path.abspath("dashboard.html")
    webbrowser.open(f"file://{dashboard_path}")
    time.sleep(2)
    
    speak("Hello! I'm JARVIS. Your dashboard is open. Ask me about weather, time, priorities, emails, or anything else!")
    
    failed_attempts = 0
    
    while True:
        user_input = listen()
        
        if user_input:
            failed_attempts = 0
            
            if "exit" in user_input.lower() or "quit" in user_input.lower():
                speak("Goodbye! Have a great day!")
                break
            
            response = get_ai_response(user_input)
            speak(response)
        else:
            failed_attempts += 1
            if failed_attempts >= 3:
                speak("I'm having trouble hearing.")
                failed_attempts = 0

if __name__ == "__main__":
    main()