# InspireWorks IVR Demo — Plivo Voice API

A multi-level Interactive Voice Response (IVR) system built with **Python/Flask** and **Plivo Voice API**. Demonstrates outbound calling, OTP-based caller authentication, language selection, audio playback, and live call forwarding.

## Features

- **Outbound Call** — Initiates a call from a Plivo number to a target phone
- **OTP Authentication** — Caller must enter their birthdate in DDMM format (4-digit DTMF)
- **Multi-level IVR Menu**
  - **Level 1**: Language selection (English / Spanish)
  - **Level 2**: Play audio message or connect to a live associate
- **Invalid Input Handling** — Re-prompts on incorrect input at every level
- **Simple Web Frontend** — One-click call trigger at `http://localhost:5000/`

## Architecture

```
Phone Call Flow:
  /make_call → Plivo API → Phone rings
       ↓
  /answer → OTP prompt (4-digit DTMF)
       ↓
  /verify_otp → Correct? → /language (Level 1)
       |                      ↓
       └── Wrong? → Re-prompt  Press 1 → /english_menu (Level 2)
                                Press 2 → /spanish_menu (Level 2)
                                              ↓
                                        Press 1 → Audio playback
                                        Press 2 → Call forwarding
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3, Flask |
| Voice API | Plivo (XML-based call flow) |
| Tunneling | ngrok (expose localhost to Plivo) |
| Frontend | Vanilla HTML/CSS/JS (embedded in Flask) |

## Prerequisites

- Python 3.8+
- [ngrok](https://ngrok.com/download) installed
- Plivo account with Auth ID & Auth Token

## Plivo Credentials

| Key | Value |
|-----|-------|
| Auth ID | `YOUR_PLIVO_AUTH_ID` |
| Auth Token | `YOUR_PLIVO_AUTH_TOKEN` |
| Plivo Number | `+91 22 6423 2030` |
| Associate Number | `022 6423 6412` |

## Setup & Run

### 1. Clone / Extract

```bash
cd ~/Desktop/plivo-ivr
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask plivo
```

### 4. Start Flask Server (Terminal 1)

```bash
source venv/bin/activate
python3 app.py
```

You should see: `Running on http://127.0.0.1:5000`

### 5. Start ngrok (Terminal 2)

```bash
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL from the output.

### 6. Update BASE_URL

Open `app.py` and replace:

```python
BASE_URL = "https://YOUR_NGROK_URL"
```

with your actual ngrok URL, e.g.:

```python
BASE_URL = "https://abc123.ngrok-free.app"
```

### 7. Restart Flask

Press `Ctrl+C` in Terminal 1, then run `python3 app.py` again.

### 8. Trigger Call

Open your browser and go to:

```
http://localhost:5000/
```

Click **"Initiate Call"** (or go directly to `http://localhost:5000/make_call`).

## Testing Flow

| Step | Action | Expected |
|------|--------|----------|
| 1 | Call arrives on phone | Answer the call |
| 2 | Enter `1111` (wrong OTP) | Bot says "Incorrect OTP, try again" |
| 3 | Enter `1503` (correct OTP) | Bot says "Authentication successful" |
| 4 | Press `1` | English language selected |
| 5 | Press `1` | Audio message plays |
| 6 | (Or) Press `2` | Call forwards to live associate |

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `source venv/bin/activate && pip install flask plivo` |
| `Address already in use` | `lsof -i :5000` then `kill -9 <PID>` |
| Call not happening | Check ngrok URL is correct, Flask is running, phone format is right |
| OTP not working | Ensure you're entering digits via dialpad (DTMF), not speaking |

## OTP Details

The OTP is the developer's birthdate in **DDMM** format.  
Example: March 15 → `1503`  
Hardcoded value: `1503`

## Demo Video Checklist

- [ ] Start Flask server
- [ ] Start ngrok tunnel
- [ ] Open web UI / trigger call
- [ ] Phone rings → Answer
- [ ] Enter wrong OTP → Re-prompted
- [ ] Enter correct OTP → Authenticated
- [ ] Select English (Press 1)
- [ ] Play audio (Press 1)
- [ ] Show call forwarding (Press 2)
