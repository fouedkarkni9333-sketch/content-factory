import os
from flask import Flask, jsonify, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# قراءة مفتاح الذكاء الاصطناعي بشكل آمن من إعدادات السيرفر
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
  genai.configure(api_key=API_KEY)

# استخدام أحدث نموذج Gemini 2.5 لتوليد النصوص الفيروسية بسرعة واحترافية
model = genai.GenerativeModel("gemini-2.5-flash")

# قائمة شاملة تضم أكثر من 30 لغة عالمية لتغطية كافة شعوب العالم
WORLD_LANGUAGES = {
    "ar": "العربية (Arabic)",
    "en": "الإنجليزية (English)",
    "fr": "الفرنسية (French)",
    "es": "الإسبانية (Spanish)",
    "de": "الألمانية (German)",
    "it": "الإيطالية (Italian)",
    "ru": "الروسية (Russian)",
    "zh": "الصينية (Chinese)",
    "ja": "اليابانية (Japanese)",
    "hi": "الهندية (Hindi)",
    "pt": "البرتغالية (Portuguese)",
    "tr": "التركية (Turkish)",
    "ko": "الكورية (Korean)",
    "nl": "الهولندية (Dutch)",
    "pl": "البولندية (Polish)",
    "sv": "السويدية (Swedish)",
    "vi": "الفيتنامية (Vietnamese)",
    "id": "الإندونيسية (Indonesian)",
    "fa": "الفارسية (Persian)",
    "ur": "الأردية (Urdu)",
    "uk": "الأوكرانية (Ukrainian)",
    "el": "اليونانية (Greek)",
    "he": "العبرية (Hebrew)",
    "ro": "الرومانية (Romanian)",
    "hu": "المجرية (Hungarian)",
    "cs": "التشيكية (Czech)",
    "da": "الدنماركية (Danish)",
    "fi": "الفنلندية (Finnish)",
    "no": "النرويجية (Norwegian)",
    "th": "التايلاندية (Thai)",
    "ms": "الملايوية (Malay)",
    "bn": "البنغالية (Bengali)",
    "sw": "السواحلية (Swahili)",
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Content Factory - 30+ Languages</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; direction: rtl; }
        .container { max-width: 700px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h2 { color: #38bdf8; text-align: center; margin-bottom: 25px; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #94a3b8; }
        select, input[type="text"] { width: 100%; padding: 14px; margin-top: 8px; background: #0f172a; color: #fff; border: 1px solid #334155; border-radius: 8px; font-size: 15px; }
        .btn-global { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; border: none; padding: 16px 20px; margin-top: 30px; width: 100%; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-global:hover { opacity: 0.9; transform: translateY(-2px); }
        #result { margin-top: 30px; background: #0f172a; padding: 25px; border-radius: 10px; white-space: pre-wrap; border-right: 6px solid #38bdf8; line-height: 1.8; font-size: 15px; }
        .platform-tags { display: flex; gap: 10px; margin-top: 10px; justify-content: center; color: #38bdf8; font-size: 13px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>مصنع المحتوى العالمي الفائق 🌍🚀</h2>
        <div class="platform-tags">
            <span>📺 YouTube Shorts</span> | <span>📸 Instagram Reels</span> | <span>🎵 TikTok</span>
        </div>
        <form>
            <label>أدخل فكرة الفيديو العامة:</label>
            <input type="text" id="topic" placeholder="مثال: أسرار وخفايا الذكاء الاصطناعي" required>
            
            <label>اختر لغة الجمهور المستهدف (أكثر من 30 لغة عالمية):</label>
            <select id="lang">
                {% for code, name in languages.items() %}
                <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
            </select>
            
            <button type="button" class="btn-global" onclick="generateContent()">⚡ توليد المحتوى العالمي بضغطة زر</button>
        </form>
        
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        async function generateContent() {
            const topic = document.getElementById('topic').value;
            const lang = document.getElementById('lang').value;
            const resDiv = document.getElementById('result');
            
            if(!topic) { alert('الرجاء إدخال الفكرة أو الموضوع أولاً'); return; }

            resDiv.style.display = 'block';
            resDiv.innerHTML = '🔄 جاري توليد السيناريو العالمي باللغة المطلوبة...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic, lang })
                });
                const data = await response.json();
                if(data.success) {
                    resDiv.innerHTML = `<b>🌐 اللغة المستهدفة:</b> ${data.lang_name}<br><b>🎯 الموضوع:</b> ${data.topic}<br><br><b>🎬 السيناريو الاحترافي (جاهز لـ TikTok, Reels, Shorts):</b><br><hr style="border-color: #334155; margin: 15px 0;">${data.script}<br><br><b>🏷️ الهاشتاغات:</b><br><span style="color: #38bdf8;">${data.hashtags}</span>`;
                } else {
                    resDiv.innerHTML = '⚠️ خطأ: ' + (data.error || 'تأكد من إعداد المفتاح في المنصة');
                }
            } catch(e) {
                resDiv.innerHTML = '❌ خطأ في الاتصال بالخادم.';
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  return render_template_string(HTML_PAGE, languages=WORLD_LANGUAGES)


@app.route("/generate", methods=["POST"])
def generate():
  try:
    data = request.json or {}
    lang_code = data.get("lang", "en")
    topic = data.get("topic", "Technology")
    lang_name = WORLD_LANGUAGES.get(lang_code, "English")

    prompt = (
        f"You are a professional global content creator for TikTok, Instagram"
        f" Reels, and YouTube Shorts. Create a viral video script about"
        f" '{topic}', written 100% in {lang_name}. Structure it with a powerful"
        " hook, core storytelling, and a clear call to action. Provide 5 viral"
        f" hashtags in {lang_name}."
    )

    response = model.generate_content(prompt)
    script = (
        response.text
        if response and response.text
        else "Failed to generate."
    )
    hashtags = f"#{topic.replace(' ', '')} #Viral #Shorts #Reels #TikTok #{lang_code.upper()}"

    return jsonify({
        "success": True,
        "lang_name": lang_name,
        "topic": topic,
        "script": script,
        "hashtags": hashtags,
    })
  except Exception as e:
    return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
