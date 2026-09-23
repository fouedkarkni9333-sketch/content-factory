from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os
import sqlite3
import requests
from gtts import gTTS
import time
import json as pyjson

app = Flask(__name__)

DB_FILE = "core_content_factory.db"
GEMINI_API_KEY = "AQ.Ab8RN6J3WsWtB2umoB1J7yvyursUBVbGLCcsXwsMlRq1MXggag"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            title TEXT,
            script TEXT,
            audio_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

dashboard_html = '''
<!doctype html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>مصنع المحتوى السحابي الذكي</title>
    <style>
        :root { background: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; }
        body { margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        h1 { text-align: center; color: #38bdf8; }
        .box { background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #334155; text-align: center; }
        button { background: #0284c7; color: #fff; border: none; padding: 14px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%; }
        button:hover { background: #0369a1; }
        .card { background: #1e293b; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-right: 4px solid #38bdf8; }
        audio { width: 100%; margin-top: 10px; filter: invert(1); }
        .time { font-size: 11px; color: #94a3b8; float: left; }
    </style>
</head>
<body>
    <div class="container">
        <h1>☁️ مصنع المحتوى (يعمل على السحاب)</h1>
        
        <div class="box">
            <h3>توليد محتوى جديد عبر Gemini AI</h3>
            <form method="POST" action="/generate">
                <button type="submit">توليد وانتاج صوتي الآن 🚀</button>
            </form>
        </div>

        <h2>📂 أرشيف المحتوى المنتج</h2>
        {% if items %}
            {% for item in items %}
            <div class="card">
                <span class="time">{{ item[5] }}</span>
                <h3>{{ item[2] }} <span style="font-size: 12px; color: #38bdf8;">({{ item[1] }})</span></h3>
                <p><strong>السكريبت:</strong> {{ item[3] }}</p>
                <audio controls>
                    <source src="/audio/{{ item[4] }}?t={{ time_now }}" type="audio/mp3">
                </audio>
            </div>
            {% endfor %}
        {% else %}
            <p style="text-align: center; color: #94a3b8;">لا يوجد محتوى بعد، اضغط على زر التوليد للبدء.</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, language, title, script, audio_file, created_at FROM projects ORDER BY id DESC LIMIT 10')
    items = cursor.fetchall()
    conn.close()
    return render_template_string(dashboard_html, items=items, time_now=int(time.time()))

@app.route('/generate', methods=['POST'])
def generate():
    title = "ابتكار رقمي ذكي"
    script = "الذكاء الاصطناعي يغير طريقة تفاعلنا مع التكنولوجيا الحديثة."
    language = "Arabic"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        prompt = "Write a short, viral 1-sentence video script and a catchy title about future technology in Arabic. Return ONLY valid JSON with keys: 'title' and 'script'."
        
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            res_body = response.json()
            text_response = res_body['candidates'][0]['content']['parts'][0]['text'].strip()
            
            if text_response.startswith("```json"):
                text_response = text_response[7:-3].strip()
            elif text_response.startswith("```"):
                text_response = text_response[3:-3].strip()
                
            parsed = pyjson.loads(text_response)
            title = parsed.get("title", title)
            script = parsed.get("script", script)
    except Exception as e:
        print(f"Gemini API Error: {e}")

    filename = f"audio_{int(time.time())}.mp3"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    try:
        tts = gTTS(text=script, lang="ar", slow=False)
        tts.save(filepath)
    except Exception as e:
        print(f"TTS Error: {e}")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (language, title, script, audio_file)
            VALUES (?, ?, ?, ?)
        ''', (language, title, script, filename))
        conn.commit()
        conn.close()
    except Exception as db_e:
        print(f"DB Error: {db_e}")

    return redirect(url_for('home'))

@app.route('/audio/<filename>')
def serve_audio(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
