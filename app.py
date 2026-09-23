from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# قائمة شاملة تضم لغات العالم أجمع مع تحديد الثقافة أو الجمهور المستهدف
WORLD_LANGUAGES = {
    "ar": {"name": "العربية (Arabic)", "region": "الوطن العربي"},
    "en": {"name": "الإنجليزية (English)", "region": "الولايات المتحدة / بريطانيا"},
    "fr": {"name": "الفرنسية (French)", "region": "فرنسا / كندا"},
    "es": {"name": "الإسبانية (Spanish)", "region": "إسبانيا / أمريكا اللاتينية"},
    "de": {"name": "الألمانية (German)", "region": "ألمانيا"},
    "it": {"name": "الإيطالية (Italian)", "region": "إيطاليا"},
    "ru": {"name": "الروسية (Russian)", "region": "روسيا"},
    "zh": {"name": "الصينية (Chinese)", "region": "الصين"},
    "ja": {"name": "اليابانية (Japanese)", "region": "اليابان"},
    "hi": {"name": "الهندية (Hindi)", "region": "الهند"},
    "pt": {"name": "البرتغالية (Portuguese)", "region": "البرتغال / البرازيل"},
    "tr": {"name": "التركية (Turkish)", "region": "تركيا"},
    "ko": {"name": "الكورية (Korean)", "region": "كوريا الجنوبية"},
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

# تصحيح هيكل اللغات البسيط لتجنب أي أخطاء برمجية
FORMATTED_LANGUAGES = {}
for code, val in WORLD_LANGUAGES.items():
    if isinstance(val, dict):
        FORMATTED_LANGUAGES[code] = val["name"]
    else:
        FORMATTED_LANGUAGES[code] = val

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مصنع المحتوى العالمي الذكي</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; direction: rtl; }
        .container { max-width: 650px; margin: 0 auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
        h2 { color: #4CAF50; text-align: center; margin-bottom: 20px; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #b0bec5; }
        select, input[type="text"] { width: 100%; padding: 12px; margin-top: 8px; background: #2d2d2d; color: #fff; border: 1px solid #444; border-radius: 6px; font-size: 14px; }
        button { background: #4CAF50; color: white; border: none; padding: 14px 20px; margin-top: 25px; width: 100%; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #45a049; }
        #result { margin-top: 25px; background: #252525; padding: 20px; border-radius: 8px; white-space: pre-wrap; border-right: 5px solid #4CAF50; line-height: 1.6; font-size: 14px; }
        .section-title { color: #81c784; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>مصنع المحتوى العالمي الذكي 🌍</h2>
        <form id="contentForm">
            <label for="topic">موضوع الفيديو أو الفكرة العامة:</label>
            <input type="text" id="topic" name="topic" placeholder="مثال: أسرار التكنولوجيا الحديثة الذكية" required>
            
            <label for="lang">اختر لغة وجمهور الدولة المستهدفة:</label>
            <select id="lang" name="lang">
                {% for code, name in languages.items() %}
                <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
            </select>
            
            <button type="button" onclick="generateContent()">توليد السيناريو والقصة الاحترافية</button>
        </form>
        
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        async function generateContent() {
            const topic = document.getElementById('topic').value;
            const lang = document.getElementById('lang').value;
            const resultDiv = document.getElementById('result');
            
            if(!topic) {
                alert('الرجاء إدخال الموضوع أولاً');
                return;
            }

            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 جاري توليد وهيكلة القصة والسيناريو والكلمات المفتاحية للجمهور المستهدف...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topic, lang: lang })
                });
                const data = await response.json();
                if(data.success) {
                    resultDiv.innerHTML = `
                        📚 <span class="section-title">اللغة والجمهور:</span> ${data.selected_language_name}<br>
                        🎯 <span class="section-title">الموضوع الأساسي:</span> ${data.topic}<br><br>
                        ✍️ <span class="section-title">السيناريو والقصة المولدة (مخصصة للجمهور المحلي):</span><br>${data.script}<br><br>
                        🏷️ <span class="section-title">الكلمات المفتاحية (Hashtags & Tags):</span><br>${data.hashtags}<br><br>
                        🚀 <span class="section-title">المنصات الجاهزة للنشر الفوري:</span> ${data.platforms_ready.join(', ')}
                    `;
                } else {
                    resultDiv.innerHTML = '❌ حدث خطأ أثناء التوليد.';
                }
            } catch (error) {
                resultDiv.innerHTML = '❌ خطأ في الاتصال بالخادم المحلي.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, languages=FORMATTED_LANGUAGES)

@app.route('/generate', methods=['POST'])
def generate_global_content():
    data = request.json or {}
    lang = data.get('lang', 'ar')
    topic = data.get('topic', 'Technology')
    
    if lang not in FORMATTED_LANGUAGES:
        return jsonify({"error": "Language not supported"}), 400

    lang_name = FORMATTED_LANGUAGES[lang]

    # محاكاة محتوى ذكي ومخصص حسب اللغة المطلوبة لضمان استهداف جمهور الدولة المحددة بدقة
    simulated_scripts = {
        "ar": f"مقدمة مشوقة جداً حول {topic} موجهة لجمهور الوطن العربي لجذب الانتباه في أول ثوانٍ، تليها حبكة سريعة ثم دعوة واضحة للتفاعل.",
        "en": f"An engaging viral hook about {topic} tailored specifically for US and global English-speaking audiences, designed for high retention and fast pacing.",
        "fr": f"Une introduction captivante sur {topic} conçue pour capter l'attention du public francophone en France et au Канада.",
        "zh": f"关于{topic}的吸引人开场白，专为中国社交媒体受众（抖音/快手风格）量身打造，节奏快且直击痛点。",
        "ja": f"{topic}に関する魅力的でスピード感のある台本。日本の視聴者の興味を惹きつける構成になっています。"
    }

    script_text = simulated_scripts.get(lang, f"Professional localized script and story breakdown for the topic '{topic}' optimized for the target culture in {lang_name}.")
    hashtags = f"#{topic.replace(' ', '')} #Viral #ForYou #{lang.upper()}Content #Trending"

    return jsonify({
        "success": True,
        "selected_language_code": lang,
        "selected_language_name": lang_name,
        "topic": topic,
        "script": script_text,
        "hashtags": hashtags,
        "platforms_ready": ["TikTok", "Instagram Reels", "YouTube Shorts"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
