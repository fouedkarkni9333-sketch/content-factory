import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

WORLD_LANGUAGES = {
    "ar": "Arabic",
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "hi": "Hindi",
    "pt": "Portuguese",
    "tr": "Turkish",
    "ko": "Korean",
    "nl": "Dutch",
    "pl": "Polish",
    "sv": "Swedish",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "fa": "Persian",
    "ur": "Urdu",
    "uk": "Ukrainian",
    "el": "Greek",
    "he": "Hebrew",
    "ro": "Romanian",
    "hu": "Hungarian",
    "cs": "Czech",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
    "th": "Thai",
}

# قوالب متجددة وآمنة لجميع اللغات لتوليد محتوى فريد
TEMPLATES = [
    "Amazing insights about {topic} tailored for local audience in {lang}. Discover the secrets that change everything.",
    "The shocking truth about {topic} in {lang}. Why everyone is talking about this massive trend right now.",
    "Everything you know about {topic} is about to change. A complete unique breakdown in {lang}.",
]


def generate_script(lang_name, topic):
  base_template = random.choice(TEMPLATES)
  script = (
      f"{base_template.format(topic=topic, lang=lang_name)}\n\n- Step 1: High"
      f" retention hook for {topic}.\n- Step 2: Core value and storytelling"
      f" in {lang_name}.\n- Step 3: Call to action for maximum engagement."
  )
  hashtags = f"#{topic.replace(' ', '')} #Viral #ForYou #{lang_name} #Trending"
  return script, hashtags


HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Content Factory</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; direction: rtl; }
        .container { max-width: 650px; margin: 0 auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
        h2 { color: #4CAF50; text-align: center; margin-bottom: 20px; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #b0bec5; }
        select, input[type="text"] { width: 100%; padding: 12px; margin-top: 8px; background: #2d2d2d; color: #fff; border: 1px solid #444; border-radius: 6px; font-size: 14px; }
        button { background: #4CAF50; color: white; border: none; padding: 14px 20px; margin-top: 25px; width: 100%; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button:hover { background: #45a049; }
        #result { margin-top: 25px; background: #252525; padding: 20px; border-radius: 8px; white-space: pre-wrap; border-right: 5px solid #4CAF50; line-height: 1.6; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>مصنع المحتوى العالمي الذكي 🌍</h2>
        <form>
            <label>موضوع الفيديو أو الفكرة العامة:</label>
            <input type="text" id="topic" placeholder="Example: AI Secrets" required>
            
            <label>اختر اللغة المستهدفة:</label>
            <select id="lang">
                {% for code, name in languages.items() %}
                <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
            </select>
            
            <button type="button" onclick="sendRequest()">توليد سيناريو فريد ومتجدد</button>
        </form>
        
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        async function sendRequest() {
            const topic = document.getElementById('topic').value;
            const lang = document.getElementById('lang').value;
            const resDiv = document.getElementById('result');
            
            if(!topic) { alert('الرجاء إدخال الموضوع'); return; }

            resDiv.style.display = 'block';
            resDiv.innerHTML = '🔄 جاري توليد السيناريو...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic, lang })
                });
                const data = await response.json();
                if(data.success) {
                    resDiv.innerHTML = `<b>Language:</b> ${data.lang_name}<br><b>Topic:</b> ${data.topic}<br><br><b>Script:</b><br>${data.script}<br><br><b>Tags:</b><br>${data.hashtags}`;
                } else {
                    resDiv.innerHTML = 'حدث خطأ في الخادم.';
                }
            } catch(e) {
                resDiv.innerHTML = 'خطأ في الاتصال بالخادم.';
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
  data = request.json or {}
  lang_code = data.get("lang", "en")
  topic = data.get("topic", "Technology")

  lang_name = WORLD_LANGUAGES.get(lang_code, "English")
  script, hashtags = generate_script(lang_name, topic)

  return jsonify({
      "success": True,
      "lang_name": lang_name,
      "topic": topic,
      "script": script,
      "hashtags": hashtags,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
