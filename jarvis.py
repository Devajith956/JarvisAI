
#### ------------------ JARVIS AI(Made By Devajith) -------------------

from flask import Flask, request, jsonify, render_template_string
import pyttsx3
import wikipedia
import os
import pyautogui
import psutil
import requests
import random
import threading
import cohere

""" This is the just a beta version of Jarvis Ai,Hope U enjoy it <3. It's my 1 year project.
    Contact me for any Errors or bugs. Make Sure to change the API KEY For the COHERE,
    And if you want accurate wheather result of ur location then change the city Also.
    The Voice is Just Terrable just ignore that, the second version will be coming with Eleven Labs.
"""

COHERE_API_KEY = "PASTE_YOUR_KEY"  # Dont forget to change the API Key
co = cohere.Client(COHERE_API_KEY)
app = Flask(__name__)
engine = pyttsx3.init()
engine.setProperty("rate", 175)
sound_enabled = True

def speak(text):
    global sound_enabled
    print("Jarvis:", text)
    if not sound_enabled:
        return
    engine.say(text)
    engine.runAndWait()

def battery_status():
    b = psutil.sensors_battery()
    if b is None:
        return "Battery: No battery detected (desktop mode)"
    return f"Battery {b.percent}% {'🔌' if b.power_plugged else '🔋'}"

def system_status():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return f"CPU {cpu}% RAM {mem}%"

def get_weather(city="Delhi"): # Change the the city
    try:
        return requests.get(f"https://wttr.in/{city}?format=3").text.strip()
    except:
        return "Weather service unavailable"

def ai_chat(prompt):
    try:
        r = co.chat(model="command-r", message=prompt)
        return r.text
    except Exception as e:
        print(e)
        return "Nahh It's Working For You And Me Either"

def handle_command(command):
    c = command.lower()
    if "battery" in c:
        response = battery_status()
    elif "system" in c:
        response = system_status()
    elif "weather" in c:
        response = get_weather()
    elif "screenshot" in c:
        f = f"shot{random.randint(1,999)}.png"
        pyautogui.screenshot().save(f)
        response = f"Screenshot saved as {f}"
    elif "wikipedia" in c:
        try:
            response = wikipedia.summary(c.replace("wikipedia", "").strip(), 2)
        except:
            response = "No Wikipedia results found."
    elif "who are you" in c or "who r u" in c or "who are u" in c or "introduce yourself" in c:
        response = "I am Jarvis, sir. A highly advanced artificial intelligence designed to assist you. My core is powered by neural networks and I am here to make your life easier — whether it's managing systems, answering questions, or just having a conversation."
    else:
        response = ai_chat(command)
    
    speak(response)
    return response

@app.route("/toggle_sound", methods=["POST"])
def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    return jsonify({"sound": sound_enabled})

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({
        "battery": battery_status(),
        "system": system_status(),
        "weather": get_weather()
    })

html_page = """
<!DOCTYPE html>
<html>
<head>
<title>Jarvis Neural Core</title>
<style>
:root {
    --bg: #0a0f1c;
    --panel: rgba(255,255,255,0.09);
    --text: #e2e8f0;
    --accent: #00f5ff;
    --glass-border: rgba(0,245,255,0.18);
}
.light {
    --bg: #f8fafc;
    --panel: rgba(10,15,28,0.09);
    --text: #111827;
    --accent: #00b8d4;
    --glass-border: rgba(0,184,212,0.18);
}
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    overflow: hidden;
    height: 100vh;
}
canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.65; }

.top-bar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 68px;
    background: var(--panel);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    padding: 0 32px;
    z-index: 100;
    box-shadow: 0 4px 30px rgba(0,245,255,0.12);
}
.logo {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 29px;
    font-weight: 700;
    letter-spacing: -1.6px;
    text-shadow: 0 0 20px var(--accent);
}
.core-small {
    width: 42px; height: 42px;
    border-radius: 50%;
    border: 3px solid var(--accent);
    animation: spin 5s linear infinite;
    box-shadow: 0 0 30px var(--accent), inset 0 0 20px var(--accent);
}

.sidebar {
    position: fixed;
    top: 68px; left: 0; bottom: 0;
    width: 280px;
    background: var(--panel);
    backdrop-filter: blur(24px);
    border-right: 1px solid var(--glass-border);
    padding: 28px;
    display: flex;
    flex-direction: column;
    z-index: 90;
}
.sidebar-header {
    font-size: 14px;
    font-weight: 600;
    opacity: 0.85;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.floating-core {
    display: flex;
    justify-content: center;
    margin: 24px 0 48px;
}
.core {
    width: 158px; height: 158px;
    border-radius: 50%;
    border: 5px solid var(--accent);
    animation: spin 7s linear infinite;
    box-shadow: 0 0 60px var(--accent), inset 0 0 40px rgba(0,245,255,0.5);
    position: relative;
}
.core::before {
    content: '';
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    border: 3px solid var(--accent);
    opacity: 0.25;
    animation: spin 14s linear infinite reverse;
}

.quick-actions button {
    width: 100%;
    padding: 15px 20px;
    margin-bottom: 10px;
    background: rgba(255,255,255,0.07);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    color: var(--text);
    font-size: 15px;
    text-align: left;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
}
.quick-actions button:hover {
    background: var(--accent);
    color: #000;
    transform: translateX(6px) scale(1.02);
}

.chat-panel {
    position: fixed;
    top: 68px; left: 280px; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    z-index: 10;
}
.chat-header {
    padding: 22px 36px;
    background: var(--panel);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 19px;
    font-weight: 600;
}

#voice-visualizer {
    display: none;
    background: rgba(0,245,255,0.15);
    border-radius: 16px;
    padding: 8px 14px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 0 30px rgba(0,245,255,0.45);
}
#voice-waveform {
    width: 280px;
    height: 52px;
}

#chat {
    flex: 1;
    overflow-y: auto;
    padding: 36px;
    display: flex;
    flex-direction: column;
    gap: 28px;
}
.message {
    max-width: 72%;
    padding: 18px 26px;
    border-radius: 24px;
    box-shadow: 0 10px 35px rgba(0,245,255,0.18);
}
.message.ai {
    align-self: flex-start;
    background: var(--panel);
    border-bottom-left-radius: 8px;
    border: 1px solid var(--glass-border);
}
.message.user {
    align-self: flex-end;
    background: linear-gradient(90deg, #00f5ff, #00b8d4);
    color: #000;
    border-bottom-right-radius: 8px;
}
.msg-content {
    line-height: 1.55;
    font-size: 16.5px;
    word-break: break-word;
}

.input-bar {
    padding: 24px 36px;
    background: var(--panel);
    backdrop-filter: blur(24px);
    border-top: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    gap: 14px;
}
.input-bar input {
    flex: 1;
    padding: 18px 28px;
    border-radius: 9999px;
    outline: none;
    border: 1px solid var(--glass-border);
    background: rgba(255,255,255,0.08);
    color: var(--text);
    font-size: 17px;
}
.input-bar input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 5px rgba(0,245,255,0.25);
}
.mic, .send-btn {
    width: 60px; height: 60px;
    border-radius: 50%;
    background: var(--accent);
    color: #000;
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    cursor: pointer;
    transition: all 0.25s;
}
.mic:hover, .send-btn:hover { transform: scale(1.15); }

.online-group {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-left: auto;
}
.dot { width: 11px; height: 11px; border-radius: 50%; box-shadow: 0 0 15px var(--accent); }
.online { background: #22c55e; }
.offline { background: #ef4444; }

.sound-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 28px;
    cursor: pointer;
    padding: 10px;
    transition: all 0.3s;
    width: 52px; height: 52px;
    border-radius: 50%;
}
.sound-btn:hover { background: rgba(0,245,255,0.2); transform: scale(1.18); }
.sound-btn.muted { color: #ff2d55; animation: mutePulse 1.6s infinite; }

@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes mutePulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

/* SCROLLBAR */
#chat::-webkit-scrollbar { width: 6px; }
#chat::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 20px; }
</style>
</head>
<body>

<canvas id="bg"></canvas>

<div class="top-bar">
    <div class="logo">
        <div class="core-small"></div>
        JARVIS
    </div>

    <div class="online-group">
        <span id="dot" class="dot online"></span>
        <span id="status">Neural Link Active</span>
        
        <button id="sound-btn" class="sound-btn" onclick="toggleSound()" title="Mute / Unmute Jarvis">🔊</button>
        <button onclick="toggleMode()" style="background:none;border:none;color:var(--text);font-size:24px;cursor:pointer;padding:10px;">🌗</button>
    </div>
</div>

<!-- SIDEBAR -->
<div class="sidebar">
    <div class="sidebar-header">Neural Core Systems</div>
    
    <div class="floating-core">
        <div class="core"></div>
    </div>

    <div class="quick-actions">
        <h3>INSTANT COMMANDS</h3>
        <button onclick="quickCommand('battery status')">🔋 Battery Status</button>
        <button onclick="quickCommand('system status')">💻 System Status</button>
        <button onclick="quickCommand('weather')">🌤️ Current Weather</button>
        <button onclick="quickCommand('screenshot')">📸 Take Screenshot</button>
        <button onclick="quickCommand('hello jarvis')">👋 Say Hello</button>
        <button onclick="quickCommand('wikipedia artificial intelligence')">📚 Wikipedia Search</button>
    </div>

    <div style="margin-top:auto;padding-top:24px;">
        <button onclick="clearChat()" style="width:100%;padding:16px;background:rgba(255,255,255,0.08);border:1px solid var(--glass-border);border-radius:14px;color:var(--text);cursor:pointer;">
            🗑️ Clear Neural Memory
        </button>
    </div>
</div>

<div class="chat-panel">
    <div class="chat-header">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:28px;">🤖</span>
            Jarvis Neural Assistant
        </div>
        
        <div id="voice-visualizer">
            <canvas id="voice-waveform" width="280" height="52"></canvas>
        </div>
    </div>

    <div id="chat"></div>

    <div class="input-bar">
        <input id="cmd" type="text" placeholder="Speak your command..." 
               onkeypress="if(event.keyCode===13) sendCommand()">
        <button class="mic" onclick="startVoice()">🎤</button>
        <button class="send-btn" onclick="sendCommand()">➤</button>
    </div>
</div>

<script>
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");
let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

for (let i = 0; i < 110; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        size: Math.random() * 2.8 + 1.2
    });
}

function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
    ctx.shadowBlur = 8;
    ctx.shadowColor = accent;
    
    for (let p of particles) {
        ctx.fillStyle = accent;
        ctx.fillRect(p.x, p.y, p.size, p.size);
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
    }
    requestAnimationFrame(drawParticles);
}
drawParticles();

const chatContainer = document.getElementById("chat");

function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    const isUser = sender === "user";
    div.innerHTML = `
        <div style="display:flex;align-items:center;gap:10px;font-size:14px;margin-bottom:8px;opacity:0.9;">
            <span style="font-size:22px;">${isUser ? "👤" : "🤖"}</span>
            <strong>${isUser ? "You" : "Jarvis"}</strong>
        </div>
        <div class="msg-content"></div>
    `;
    chatContainer.appendChild(div);
    const content = div.querySelector(".msg-content");
    if (isUser) content.textContent = text;
    else {
        let i = 0;
        function type() {
            if (i < text.length) {
                content.innerHTML += text[i] === " " ? "&nbsp;" : text[i];
                i++;
                setTimeout(type, 14);
            }
        }
        type();
    }
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendCommand() {
    const input = document.getElementById("cmd");
    const command = input.value.trim();
    if (!command) return;
    addMessage("user", command);
    input.value = "";
    
    fetch("/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({command: command})
    })
    .then(r => r.json())
    .then(d => addMessage("ai", d.response));
}

function quickCommand(cmd) {
    document.getElementById("cmd").value = cmd;
    sendCommand();
}

let audioContext, analyser, dataArray, mediaStream, raf;
const visualizer = document.getElementById("voice-visualizer");
const waveCanvas = document.getElementById("voice-waveform");
const wctx = waveCanvas.getContext("2d");

function drawCoolWaveform() {
    if (!analyser) return;
    analyser.getByteFrequencyData(dataArray);
    
    wctx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
    
    const bars = 68;
    const barWidth = waveCanvas.width / bars;
    const centerY = waveCanvas.height / 2;
    
    for (let i = 0; i < bars; i++) {
        const height = (dataArray[i * 3] / 255) * (waveCanvas.height * 0.85);
        
        wctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent');
        wctx.shadowBlur = 15;
        wctx.shadowColor = getComputedStyle(document.documentElement).getPropertyValue('--accent');
        wctx.fillRect(i * barWidth, centerY - height/2, barWidth * 0.75, height);
        
        wctx.fillStyle = "rgba(255,255,255,0.25)";
        wctx.fillRect(i * barWidth, centerY + height/2 - 4, barWidth * 0.75, 4);
    }
    raf = requestAnimationFrame(drawCoolWaveform);
}

function startVoice() {
    visualizer.style.display = "flex";
    
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaStream = stream;
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        source.connect(analyser);
        dataArray = new Uint8Array(analyser.frequencyBinCount);
        
        drawCoolWaveform();
        
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SR) {
            const rec = new SR();
            rec.lang = "en-US";
            rec.onresult = e => {
                document.getElementById("cmd").value = e.results[0][0].transcript;
                sendCommand();
            };
            rec.onend = () => visualizer.style.display = "none";
            rec.start();
        }
    }).catch(() => {
        alert("Microphone access denied.");
        visualizer.style.display = "none";
    });
}

function clearChat() {
    chatContainer.innerHTML = "";
    addMessage("ai", "Neural memory cleared. Just Getting Ready, sir.");
}

let soundEnabled = true;
const soundBtn = document.getElementById("sound-btn");
function toggleSound() {
    soundEnabled = !soundEnabled;
    soundBtn.textContent = soundEnabled ? "🔊" : "🔇";
    soundBtn.classList.toggle("muted", !soundEnabled);
    fetch("/toggle_sound", {method: "POST"});
}

function toggleMode() {
    document.body.classList.toggle("light");
}

window.addEventListener("load", () => {
    setTimeout(() => addMessage("ai", "Neural core online. How may I assist you today, sir?"), 600);
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_page)

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    r = handle_command(data.get("command", ""))
    return jsonify({"response": r})

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(port=5000, debug=False)).start()
    speak("Jarvis neural systems online. Ready for command.")
