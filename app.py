from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os
import json
import random
from datetime import datetime
from gTTS import gTTS

app = Flask(__name__)

PROJECT_FILE = "dynamic_global_project.json"

TRENDING_TOPICS = [
    {
        "title": "ثورة الذكاء الاصطناعي في حياتنا اليومية",
        "script": "كيف يغير الذكاء الاصطناعي تفاصيل حياتنا اليومية وطريقة عملنا بسرعة مذهلة."
    },
    {
        "title": "أسرار التكنولوجيا العميقة ومستقبل المستقبل",
        "script": "نظرة سريعة على التقنيات الناشئة التي ستعيد صياغة مستقبل البشرية في السنوات القادمة."
    },
    {
        "title": "الابتكار الرقمي وقوة الأفكار البسيطة",
        "script": "كيف يمكن لفكرة برمجية بسيطة أن تتحول إلى نظام قوي ومؤثر بجهد فردي."
    }
]

def load_project_data():
    if os.path.exists(PROJECT_FILE):
        with open(PROJECT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

dashboard_html = '''
<!doctype html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>مصنع المحتوى الذكي</title>
    <style>
        :root { background: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; }
        body { margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: auto; }
        h1 { text-align: center; color: #38bdf8; }
        .generator-card { background: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #334155; text-align: center; }
        button { background: #0284c7; color: #fff; border: none; padding: 14px 20px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background: #0369a1; }
        .card { background: #1e293b; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-right: 5px solid #38bdf8; }
        audio { width: 100%; margin-top: 10px; filter: invert(1); }
        .lang-tag { background: #0284c7; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
        .time-tag { color: #94a3b8; font-size: 13px; margin-bottom: 5px; display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>☁️ مصنع المحتوى الذكي</h1>
        <div class="generator-card">
            <h2>🧠 توليد محتوى صوتي جديد</h2>
            <form method="POST" action="/generate">
                <button type="submit">توليد وانتاج صوتي الآن 🚀</button>
            </form>
        </div>
        <h2>📂 أرشيف المحتوى المنتج</h2>
        {% if data %}
            {% for item_id, details in data.items() %}
            <div class="card">
                <span class="time-tag">🕒 {{ details['timestamp'] }}</span>
                <h3><span>{{ details['title'] }}</span> <span class="lang-tag">{{ details['language'] }}</span></h3>
                <p><strong>السكريبت:</strong> {{ details['script'] }}</p>
                <audio controls>
                    <source src="/audio/{{ details['audio_file'] }}" type="audio/mp3">
                </audio>
            </div>
            {% endfor %}
        {% else %}
            <p style="text-align: center; color: #64748b;">لا يوجد محتوى بعد.</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    data = load_project_data()
    return render_template_string(dashboard_html, data=data)

@app.route('/generate', methods=['POST'])
def generate():
    current_content = load_project_data()
    selected_topic = random.choice(TRENDING_TOPICS)
    
    timestamp_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp_display = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audio_filename = f"audio_{timestamp_id}.mp3"
    
    try:
        tts = gTTS(text=selected_topic["script"], lang="ar", slow=False)
        tts.save(audio_filename)
        
        new_entry = {
            "language": "Arabic",
            "title": selected_topic["title"],
            "script": selected_topic["script"],
            "audio_file": audio_filename,
            "timestamp": timestamp_display
        }
        
        updated_content = {timestamp_id: new_entry}
        updated_content.update(current_content)
        
        with open(PROJECT_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_content, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: {e}")

    return redirect(url_for('home'))

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
