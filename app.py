from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# قائمة اللغات المدعومة بالكامل
SUPPORTED_LANGUAGES = {
    "ar": "العربية",
    "fr": "الفرنسية",
    "en": "الإنجليزية",
    "es": "الإسبانية",
    "it": "الإيطالية",
    "de": "الألمانية",
    "zh": "الصينية",
    "ja": "اليابانية",
    "hi": "الهندية"
}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "system": "Autonomous Content Factory",
        "supported_languages": SUPPORTED_LANGUAGES
    })

@app.route('/generate', methods=['POST'])
def generate_factory_content():
    data = request.json or {}
    lang = data.get('lang', 'ar')
    topic = data.get('topic', 'Technology')
    
    if lang not in SUPPORTED_LANGUAGES:
        return jsonify({"error": "Language not supported"}), 400

    # هيكل المحتوى التلقائي المولد حسب اللغة المطلوبة
    content_titles = {
        "ar": f"محتوى تلقائي حول: {topic}",
        "fr": f"Contenu automatique sur : {topic}",
        "en": f"Automated content about: {topic}",
        "es": f"Contenido automatizado sobre: {topic}",
        "it": f"Contenuto automatizado su: {topic}",
        "de": f"Automatisierter Inhalt über: {topic}",
        "zh": f"关于以下内容的自动内容：{topic}",
        "ja": f"自動コンテンツ： {topic}",
        "hi": f"स्वचालित सामग्री: {topic}"
    }

    generated_text = content_titles.get(lang, f"Content about {topic}")

    return jsonify({
        "success": True,
        "language": SUPPORTED_LANGUAGES[lang],
        "topic": topic,
        "generated_content": generated_text,
        "platforms_ready": ["TikTok", "Instagram", "YouTube Shorts"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
