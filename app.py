from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# قائمة شاملة تضم لغات العالم أجمع
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
    "th": "التايلاندية (Thai)"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مصنع المحتوى العالمي</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; direction: rtl; }
        .container { max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        h2 { color: #4CAF50; text-align: center; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        select, input[type="text"] { width: 100%; padding: 10px; margin-top: 5px; background: #2d2d2d; color: #fff; border: 1px solid #444; border-radius: 5px; }
        button { background: #4CAF50; color: white; border: none; padding: 12px 20px; margin-top: 20px; width: 100%; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #45a049; }
        #result { margin-top: 20px; background: #2d2d2d; padding: 15px; border-radius: 5px; white-space: pre-wrap; border-right: 4px solid #4CAF50; }
    </style>
</head>
<body>
    <div class="container">
        <h2>مصنع المحتوى العالمي الذكي</h2>
        <form id="contentForm">
            <label for="topic">موضوع المحتوى أو الفكرة:</label>
            <input type="text" id="topic" name="topic" placeholder="مثال: الذكاء الاصطناعي وتطوير المستقبل" required>
            
            <label for="lang">اختر لغة العالم المستهدفة:</label>
            <select id="lang" name="lang">
                {% for code, name in languages.items() %}
                <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
            </select>
            
            <button type="button" onclick="generateContent()">توليد المحتوى الآن</button>
        </form>
        
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        async function generateContent() {
            const topic = document.getElementById('topic').value;
            const lang = document.getElementById('lang').value;
            const resultDiv = document.getElementById('result');
            
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'جاري توليد المحتوى ومعالجة البيانات...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topic, lang: lang })
                });
                const data = await response.json();
                if(data.success) {
                    resultDiv.innerHTML = `<strong>اللغة:</strong> ${data.selected_language_name}<br><strong>الموضوع:</strong> ${data.topic}<br><br><strong>المحتوى المولد:</strong><br>${data.generated_content}<br><br><strong>المنصات الجاهزة:</strong> ${data.platforms_ready.join(', ')}`;
                } else {
                    resultDiv.innerHTML = 'حدث خطأ أثناء التوليد.';
                }
            } catch (error) {
                resultDiv.innerHTML = 'خطأ في الاتصال بالخادم.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, languages=WORLD_LANGUAGES)

@app.route('/generate', methods=['POST'])
def generate_global_content():
    data = request.json or {}
    lang = data.get('lang', 'ar')
    topic = data.get('topic', 'Technology')
    
    if lang not in WORLD_LANGUAGES:
        return jsonify({"error": "Language not supported"}), 400

    lang_name = WORLD_LANGUAGES[lang]

    return jsonify({
        "success": True,
        "selected_language_code": lang,
        "selected_language_name": lang_name,
        "topic": topic,
        "generated_content": f"تم بنجاح إعداد وهيكلة محتوى احترافي وجذاب حول موضوع: '{topic}' ومناسب للانتشار السريع باللغة {lang_name}.",
        "platforms_ready": ["TikTok", "Instagram Reels", "YouTube Shorts"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
