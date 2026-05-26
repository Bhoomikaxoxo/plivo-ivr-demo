from flask import Flask, request, Response, render_template_string
import plivo
from plivo import plivoxml

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

AUTH_ID = "YOUR_PLIVO_AUTH_ID"
AUTH_TOKEN = "YOUR_PLIVO_AUTH_TOKEN"

PLIVO_NUMBER = "912264232030"

YOUR_PHONE = "919343428889"

LIVE_ASSOCIATE = "912264236412"

CORRECT_OTP = "1503"

BASE_URL = "https://unwashed-laxative-goggles.ngrok-free.dev"


# -----------------------------
# FRONTEND (OPTIONAL UI)
# -----------------------------

FRONTEND_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InspireWorks IVR Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
        }
        .container {
            text-align: center;
            max-width: 500px;
            padding: 48px 40px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 24px 48px rgba(0,0,0,0.4);
        }
        .logo {
            font-size: 48px;
            margin-bottom: 8px;
        }
        h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 6px;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            font-size: 14px;
            color: rgba(255,255,255,0.5);
            margin-bottom: 32px;
        }
        .info-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 28px;
            text-align: left;
        }
        .info-card h3 {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.4);
            margin-bottom: 12px;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 14px;
        }
        .info-row:last-child { border-bottom: none; }
        .info-label { color: rgba(255,255,255,0.5); }
        .info-value { font-weight: 600; color: #a78bfa; }
        .call-btn {
            display: inline-block;
            padding: 16px 48px;
            font-size: 16px;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, #7c3aed, #3b82f6);
            border: none;
            border-radius: 14px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
        }
        .call-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(124, 58, 237, 0.5);
        }
        .call-btn:active { transform: translateY(0); }
        .call-btn.loading {
            opacity: 0.7;
            pointer-events: none;
        }
        #status {
            margin-top: 20px;
            font-size: 14px;
            color: rgba(255,255,255,0.6);
            min-height: 20px;
        }
        #status.success { color: #34d399; }
        #status.error { color: #f87171; }
        .flow-section {
            margin-top: 28px;
            text-align: left;
        }
        .flow-section h3 {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,0.4);
            margin-bottom: 12px;
        }
        .flow-step {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            font-size: 13px;
            color: rgba(255,255,255,0.6);
        }
        .flow-step .num {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(124, 58, 237, 0.2);
            border: 1px solid rgba(124, 58, 237, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 600;
            color: #a78bfa;
            flex-shrink: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📞</div>
        <h1>InspireWorks IVR</h1>
        <p class="subtitle">Plivo Voice API Demo System</p>

        <div class="info-card">
            <h3>Call Configuration</h3>
            <div class="info-row">
                <span class="info-label">From</span>
                <span class="info-value">+91 22 6423 2030</span>
            </div>
            <div class="info-row">
                <span class="info-label">To</span>
                <span class="info-value">+91 93434 28889</span>
            </div>
            <div class="info-row">
                <span class="info-label">OTP</span>
                <span class="info-value">Birthdate (DDMM)</span>
            </div>
        </div>

        <button class="call-btn" id="callBtn" onclick="makeCall()">
            ☎️ Initiate Call
        </button>
        <div id="status"></div>

        <div class="flow-section">
            <h3>Call Flow</h3>
            <div class="flow-step"><span class="num">1</span> Phone rings → Enter 4-digit OTP</div>
            <div class="flow-step"><span class="num">2</span> OTP verified → Language selection</div>
            <div class="flow-step"><span class="num">3</span> Press 1: English / Press 2: Spanish</div>
            <div class="flow-step"><span class="num">4</span> Press 1: Audio / Press 2: Live associate</div>
        </div>
    </div>

    <script>
        async function makeCall() {
            const btn = document.getElementById('callBtn');
            const status = document.getElementById('status');
            btn.classList.add('loading');
            btn.textContent = '⏳ Calling...';
            status.textContent = '';
            status.className = '';

            try {
                const res = await fetch('/make_call');
                const text = await res.text();
                status.textContent = '✅ ' + text;
                status.className = 'success';
            } catch (err) {
                status.textContent = '❌ Failed to initiate call';
                status.className = 'error';
            } finally {
                btn.classList.remove('loading');
                btn.textContent = '☎️ Initiate Call';
            }
        }
    </script>
</body>
</html>
"""


# -----------------------------
# HOME PAGE (FRONTEND)
# -----------------------------

@app.route("/")
def home():
    return render_template_string(FRONTEND_HTML)


# -----------------------------
# MAKE CALL
# -----------------------------

@app.route("/make_call")
def make_call():

    client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)

    response = client.calls.create(
        from_=PLIVO_NUMBER,
        to_=YOUR_PHONE,
        answer_url=f"{BASE_URL}/answer",
        answer_method="GET"
    )

    return f"Call initiated: {response.request_uuid}"


# -----------------------------
# ANSWER — OTP PROMPT
# -----------------------------

@app.route("/answer", methods=["GET", "POST"])
def answer():

    response = plivoxml.Response()

    get_digits = plivoxml.GetInput(
        action=f"{BASE_URL}/verify_otp",
        method="POST",
        input_type="dtmf",
        num_digits=4
    )

    get_digits.addSpeak(
        "Welcome to Inspire Works. Please enter your 4 digit OTP."
    )

    response.add(get_digits)

    return Response(str(response), mimetype="text/xml")


# -----------------------------
# VERIFY OTP
# -----------------------------

@app.route("/verify_otp", methods=["POST"])
def verify_otp():

    digits = request.form.get("Digits")

    print(f"OTP entered: {digits}")

    response = plivoxml.Response()

    if digits == CORRECT_OTP:

        get_lang = plivoxml.GetInput(
            action=f"{BASE_URL}/language",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_lang.addSpeak(
            "Authentication successful. "
            "Press 1 for English. "
            "Press 2 for Spanish."
        )

        response.add(get_lang)

    else:

        get_retry = plivoxml.GetInput(
            action=f"{BASE_URL}/verify_otp",
            method="POST",
            input_type="dtmf",
            num_digits=4
        )

        get_retry.addSpeak(
            "Incorrect OTP. Please try again. Enter your 4 digit OTP."
        )

        response.add(get_retry)

    return Response(str(response), mimetype="text/xml")


# -----------------------------
# LANGUAGE MENU (LEVEL 1)
# -----------------------------

@app.route("/language", methods=["POST"])
def language():

    digit = request.form.get("Digits")

    print(f"Language selected: {digit}")

    response = plivoxml.Response()

    if digit == "1":

        get_menu = plivoxml.GetInput(
            action=f"{BASE_URL}/english_menu",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_menu.addSpeak(
            "English selected. "
            "Press 1 to play an audio message. "
            "Press 2 to connect to a live associate."
        )

        response.add(get_menu)

    elif digit == "2":

        get_menu = plivoxml.GetInput(
            action=f"{BASE_URL}/spanish_menu",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_menu.addSpeak(
            "Espanol seleccionado. "
            "Presione 1 para reproducir un mensaje de audio. "
            "Presione 2 para conectarse con un asociado."
        )

        response.add(get_menu)

    else:

        get_retry = plivoxml.GetInput(
            action=f"{BASE_URL}/language",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_retry.addSpeak(
            "Invalid input. "
            "Press 1 for English. "
            "Press 2 for Spanish."
        )

        response.add(get_retry)

    return Response(str(response), mimetype="text/xml")


# -----------------------------
# ENGLISH MENU (LEVEL 2)
# -----------------------------

@app.route("/english_menu", methods=["POST"])
def english_menu():

    digit = request.form.get("Digits")

    print(f"English menu selection: {digit}")

    response = plivoxml.Response()

    if digit == "1":

        response.addSpeak("Playing audio message now.")
        response.addPlay(
            "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
        )
        response.addSpeak("Thank you for using Inspire Works. Goodbye.")

    elif digit == "2":

        response.addSpeak("Connecting you to a live associate. Please hold.")
        dial = plivoxml.Dial(callerId=PLIVO_NUMBER)
        dial.addNumber(LIVE_ASSOCIATE)
        response.add(dial)

    else:

        get_retry = plivoxml.GetInput(
            action=f"{BASE_URL}/english_menu",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_retry.addSpeak(
            "Invalid input. "
            "Press 1 to play an audio message. "
            "Press 2 to connect to a live associate."
        )

        response.add(get_retry)

    return Response(str(response), mimetype="text/xml")


# -----------------------------
# SPANISH MENU (LEVEL 2)
# -----------------------------

@app.route("/spanish_menu", methods=["POST"])
def spanish_menu():

    digit = request.form.get("Digits")

    print(f"Spanish menu selection: {digit}")

    response = plivoxml.Response()

    if digit == "1":

        response.addSpeak("Reproduciendo mensaje de audio ahora.")
        response.addPlay(
            "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
        )
        response.addSpeak("Gracias por usar Inspire Works. Adios.")

    elif digit == "2":

        response.addSpeak("Conectandote con un asociado. Por favor espera.")
        dial = plivoxml.Dial(callerId=PLIVO_NUMBER)
        dial.addNumber(LIVE_ASSOCIATE)
        response.add(dial)

    else:

        get_retry = plivoxml.GetInput(
            action=f"{BASE_URL}/spanish_menu",
            method="POST",
            input_type="dtmf",
            num_digits=1
        )

        get_retry.addSpeak(
            "Entrada invalida. "
            "Presione 1 para reproducir un mensaje de audio. "
            "Presione 2 para conectarse con un asociado."
        )

        response.add(get_retry)

    return Response(str(response), mimetype="text/xml")


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)