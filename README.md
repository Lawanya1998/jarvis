# 🤖 JARVIS - Complete Setup Guide
## Voice Assistant + 3D Hologram Dashboard

---

## What You Have

1. **jarvis.py** — Python voice assistant (reads Gmail, speaks brief, saves data)
2. **dashboard.html** — Beautiful 3D hologram interface (shows data in browser)
3. **requirements.txt** — Dependencies

---

## How It Works

```
Step 1: Run Python
────────────────
python jarvis.py
    ↓
- Connects to Gmail
- Reads your emails
- Speaks your morning brief 🎙️
- Saves data to data.json

Step 2: Open Dashboard
──────────────────────
Open dashboard.html in your browser
    ↓
- Shows your emails in 3D
- Displays priorities in hologram
- Reads data from data.json
- Auto-updates every 5 seconds
```

---

## Setup Instructions

### Prerequisites
- Python 3.7+ installed
- Environment variables set:
  ```bash
  setx GMAIL_EMAIL "your@gmail.com"
  setx GMAIL_PASSWORD "your-16-char-app-password"
  ```

### Step 1: Verify Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Jarvis (First Terminal)
```bash
cd C:\Users\YourName\Downloads\JARVIS
python jarvis.py
```

**You'll hear:**
- ✅ "Jarvis initializing"
- ✅ "Connecting to Gmail"
- ✅ "Fetching your emails"
- ✅ Your morning brief spoken aloud
- ✅ "Dashboard ready"

**Files created:**
- `data.json` — Your email data
- `jarvis_brief.txt` — Text version of brief

### Step 3: Open Dashboard (Second Terminal or Browser)
```bash
# Option A: Open file in browser
1. Find dashboard.html in your JARVIS folder
2. Double-click it
3. It opens in your default browser

# Option B: Use Python HTTP server
cd C:\Users\YourName\Downloads\JARVIS
python -m http.server 8000
# Then go to: http://localhost:8000/dashboard.html
```

### Step 4: See the Magic! ✨
- Dashboard opens with 3D hologram
- Shows YOUR real emails from Gmail
- Displays YOUR priorities
- Updates automatically

---

## Usage Flow

### Morning Routine:
1. **Terminal 1:** Run `python jarvis.py`
2. Listen to your morning brief 🎙️
3. Dashboard shows data in real-time
4. Check the 3D interface in browser
5. Get ready for the day!

### Update Data:
- Run `python jarvis.py` again anytime
- Dashboard auto-refreshes (every 5 seconds)
- New emails appear in 3D

---

## Troubleshooting

### Dashboard shows "Run jarvis.py to load data"
- Run `python jarvis.py` first
- Check that `data.json` is created in same folder
- Refresh browser (F5)

### No voice output
- Check speaker volume
- Run: `pip install pyttsx3`
- Restart Command Prompt

### Gmail not connecting
- Verify credentials set correctly
- Check app password (16 characters)
- Ensure 2-Step Verification is ON

### Data not updating
- Wait 5 seconds (auto-refresh)
- Or refresh browser manually (F5)
- Run `python jarvis.py` again

---

## Files Explained

| File | Purpose |
|------|---------|
| `jarvis.py` | Main voice assistant (reads Gmail, speaks brief) |
| `dashboard.html` | 3D hologram interface (shows data in browser) |
| `data.json` | Email data (created when jarvis.py runs) |
| `jarvis_brief.txt` | Text version of morning brief |
| `jarvis_memory.json` | Your priorities, projects, notes |
| `requirements.txt` | Python dependencies |

---

## Customizing Jarvis

### Add Your Priorities
Edit `jarvis_memory.json`:
```json
{
  "priorities": [
    "Finish Q3 report",
    "Team meeting at 2 PM",
    "Review code changes"
  ],
  "projects": [
    "Project Alpha",
    "Website redesign"
  ],
  "notes": "Focus on important tasks first"
}
```

Then run `python jarvis.py` → Priorities appear in dashboard!

### Change Voice Speed
In `jarvis.py`, find this line and adjust:
```python
engine.setProperty('rate', 150)  # 150 = normal speed (50-300 is range)
```

### Get More Emails
In `jarvis.py`, find:
```python
emails = get_recent_emails(imap)  # Default: 5
# Change to:
emails = get_recent_emails(imap, max_results=10)  # Now gets 10
```

---

## Advanced: Schedule It

### Windows Task Scheduler
1. Search for "Task Scheduler"
2. Create Basic Task:
   - Name: "Jarvis Morning Brief"
   - Trigger: Daily at 6:30 AM
   - Action: Start `python jarvis.py`
3. Every morning at 6:30 AM, Jarvis runs automatically!

---

## What's Next?

After this works:
- ✅ Add calendar integration
- ✅ Slack notifications
- ✅ Custom reminders
- ✅ Voice commands
- ✅ More animations in dashboard

---

## Questions?

**If something doesn't work:**
1. Check the error message
2. Verify all environment variables are set
3. Make sure all files are in same folder
4. Run `pip install -r requirements.txt` again
5. Restart Command Prompt and try again

You're all set! Run `python jarvis.py` and open `dashboard.html` 🚀
