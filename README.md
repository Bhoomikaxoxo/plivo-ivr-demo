# InspireWorks IVR Demo — Plivo Voice API

A multi-level Interactive Voice Response (IVR) system built with **Python/Flask** and **Plivo Voice API**.

## Features

- **Outbound Call** — Initiates a call from a Plivo number to a target phone
- **OTP Authentication** — Caller must enter their birthdate in DDMM format (4-digit DTMF)
- **Multi-level IVR Menu**
  - **Level 1**: Language selection (English / Spanish)
  - **Level 2**: Play audio message or connect to a live associate
- **Invalid Input Handling** — Re-prompts on incorrect input at every level
- **Simple Web Frontend** — One-click call trigger at `http://localhost:5001/`

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3, Flask |
| Voice API | Plivo (SDK 4.60.1) |
| Environment | `python-dotenv` |
| Tunneling | ngrok (Port 5001) |

## Setup & Run

### 1. Environment Setup

```bash
cd ~/Desktop/plivo-ivr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a file named `.env` in the root directory and add:

```env
PLIVO_AUTH_ID=your_auth_id
PLIVO_AUTH_TOKEN=your_auth_token
PLIVO_NUMBER=912264232030
YOUR_PHONE=target_phone_number
LIVE_ASSOCIATE=912264236412
BASE_URL=your_ngrok_url
CORRECT_OTP=1503
```

### 3. Start Application

1. **Terminal 1**: `python3 app.py` (Runs on port 5001)
2. **Terminal 2**: `ngrok http 5001`
3. Update `BASE_URL` in your `.env` with the ngrok URL.

### 4. Trigger Call

Open `http://localhost:5001/` in your browser and click **"Initiate Call"**.

## OTP Details

The OTP is set to `1503` (DDMM format).
