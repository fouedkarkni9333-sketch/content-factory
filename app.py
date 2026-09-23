from flask import Flask, jsonify, request

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

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "system": "Global Autonomous Content Factory",
        "total_languages": len(WORLD_LANGUAGES),
        "supported_languages": WORLD_LANGUAGES
    })

@app.route('/generate', methods=['POST'])
def generate_global_content():
    data = request.json or {}
    lang = data.get('lang', 'ar')
    topic = data.get('topic', 'Technology')
    
    if lang not in WORLD_LANGUAGES:
        return jsonify({
            "error": "Language not supported", 
            "available_languages": list(WORLD_LANGUAGES.keys())
        }), 400

    lang_name = WORLD_LANGUAGES[lang]

    return jsonify({
        "success": True,
        "selected_language_code": lang,
        "selected_language_name": lang_name,
        "topic": topic,
        "generated_content": f"Generated global automated content for topic: '{topic}' in {lang_name}",
        "platforms_ready": ["TikTok", "Instagram Reels", "YouTube Shorts"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
