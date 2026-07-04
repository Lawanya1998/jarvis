#!/usr/bin/env python3
"""
JARVIS - Local AI Assistant with Voice + 3D Dashboard
Reads Gmail, generates brief, speaks it, and saves data for web dashboard
"""

import os
import json
import imaplib
import email
from datetime import datetime, timedelta
from email.header import decode_header
import pyttsx3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

MEMORY_FILE = "jarvis_memory.json"
DATA_FILE = "data.json"  # For dashboard

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)


def speak(text):
    """Make Jarvis speak the text"""
    print(f"\n🎙️ JARVIS: {text}\n")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Voice error: {e}")


def connect_gmail():
    """Connect to Gmail using IMAP"""
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        imap.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        return imap
    except Exception as e:
        print(f"Error connecting to Gmail: {e}")
        speak("Failed to connect to Gmail. Check your credentials.")
        return None


def get_recent_emails(imap, max_results: int = 5) -> list:
    """Get recent unread emails from Gmail"""
    try:
        imap.select("INBOX")
        status, messages = imap.search(None, "UNSEEN")
        
        if status != "OK":
            return []
        
        email_ids = messages[0].split()
        email_summaries = []
        
        for email_id in email_ids[-max_results:]:
            status, msg_data = imap.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Extract subject
                    subject = msg.get("Subject", "No subject")
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    try:
                        decoded_subject = decode_header(subject)
                        subject = "".join([
                            part.decode(encoding or "utf-8") if isinstance(part, bytes) else part
                            for part, encoding in decoded_subject
                        ])
                    except:
                        pass
                    
                    # Extract sender
                    sender = msg.get("From", "Unknown sender")
                    
                    # Extract body snippet
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    snippet = body[:50].replace("\n", " ") if body else ""
                    
                    email_summaries.append({
                        "subject": subject,
                        "from": sender,
                        "snippet": snippet
                    })
        
        return email_summaries
    
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


def load_memory() -> dict:
    """Load persistent memory about the user"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"priorities": [], "projects": [], "notes": ""}


def save_dashboard_data(emails: list, memory: dict):
    """Save data for the web dashboard"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "emails": emails,
        "priorities": memory.get('priorities', []),
        "projects": memory.get('projects', []),
        "notes": memory.get('notes', ''),
        "status": "online"
    }
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Dashboard data saved to {DATA_FILE}")


def generate_morning_brief(emails: list, memory: dict) -> str:
    """Generate a formatted morning brief"""
    
    brief = "Good morning! Here's your brief.\n\n"
    
    if emails:
        brief += f"You have {len(emails)} unread emails:\n"
        for i, email_data in enumerate(emails, 1):
            brief += f"{i}. From {email_data['from']}: {email_data['subject']}\n"
    else:
        brief += "No new emails.\n"
    
    brief += "\n"
    
    if memory.get('priorities'):
        brief += "Your priorities today:\n"
        for priority in memory['priorities']:
            brief += f"- {priority}\n"
    
    brief += "\n"
    
    if memory.get('projects'):
        brief += "Active projects:\n"
        for project in memory['projects']:
            brief += f"- {project}\n"
    
    if memory.get('notes'):
        brief += f"\nNotes: {memory['notes']}\n"
    
    brief += "\nHave a productive day!"
    
    return brief


def main():
    print("🤖 JARVIS - Starting up...\n")
    
    speak("Jarvis initializing")

    if not GMAIL_EMAIL or not GMAIL_PASSWORD:
        print("❌ Error: Gmail credentials not set!")
        print("Please set these environment variables:")
        print("  setx GMAIL_EMAIL your-email@gmail.com")
        print("  setx GMAIL_PASSWORD your-app-password")
        speak("Gmail credentials not set. Please configure them.")
        return
    
    speak("Connecting to Gmail")
    print("📧 Connecting to Gmail...")
    imap = connect_gmail()
    if not imap:
        return

    print("📬 Fetching your unread emails...")
    speak("Fetching your emails")
    emails = get_recent_emails(imap)
    imap.close()
    imap.logout()

    memory = load_memory()

    print("\n✨ Generating your morning brief...\n")
    brief = generate_morning_brief(emails, memory)

    print("=" * 60)
    print(brief)
    print("=" * 60)

    # Save data for dashboard
    save_dashboard_data(emails, memory)

    # Speak the brief
    speak(brief)

    # Save to file
    with open("jarvis_brief.txt", "w") as f:
        f.write(f"Morning Brief - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n")
        f.write(brief)
        f.write("\n" + "=" * 60)

    print("\n✅ Brief saved to jarvis_brief.txt")
    print("🌐 Open dashboard.html in your browser to see the 3D interface!")
    speak("Brief complete. Dashboard ready. Have a great day!")


if __name__ == "__main__":
    main()
