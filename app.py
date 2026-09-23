import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

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
}

# قوالب ديناميكية متعددة ومتجددة لكل لغة لمنع التكرار نهائياً وتوليد سيناريوهات جذابة
DYNAMIC_TEMPLATES = {
    "ar": {
        "hooks": [
            "هل تعلم أن ما تعرفه عن {topic} قد يكون خطأً تماماً؟",
            "سر خطير لم يبرزه أحد من قبل حول عالم {topic}!",
            "لماذا يتجاهل الجميع هذه الحقيقة الصادمة عن {topic}؟",
            "تغيير جذري قادم في مستقبل {topic} سيغير كل شيء.",
        ],
        "bodies": [
            "في السنوات الأخيرة، شهدنا تطورات مذهلة جعلت {topic} محور الاتمام العالمي. الأرقام تثبت أن من يجهل هذه التفاصيل يفقد الكثير. إليك القصة الكاملة باختصار شديد وكيف يمكنك الاستفادة منها الآن.",
            "الكثيرون يبحثون عن مفتاح النجاح في {topic} دونรู้ السر الحقيقي. السر يكمن في التفاصيل الصغيرة التي تتجاهلها العادة اليومية. دعنا نكشفها لك خطوة بخطوة.",
            "إذا كنت تعتقد أنك رأيت كل شيء عن {topic}, فأنت مخطئ تماماً. التحليلات الأخيرة أثبتت أن الاتجاهات تتغير بسرعة، والجاهزية هي الفيصل الحقيقي.",
        ],
        "ctas": [
            "شارك الفيديو ليعرف أصدقاؤك الحقيقة، واكتب رأيك في التعليقات!",
            "اضغط متابعة للمزيد من الحقائق الحصرية يومياً!",
            "احفظ الفيديو لأنك ستعتاز إليه حتماً لاحقاً!",
        ],
    },
    "en": {
        "hooks": [
            "What nobody is telling you about {topic} will shock you!",
            "Everything you knew about {topic} is completely wrong.",
            "This secret about {topic} is changing everything right now.",
            "Why is everyone ignoring this massive truth regarding {topic}?",
        ],
        "bodies": [
            "Recent breakthroughs in {topic} have completely shifted the global landscape. If you are not paying attention to these details, you are falling behind. Here is the exact breakdown you need.",
            "Most people fail to understand the core mechanism of {topic}. The real power lies in the hidden variables that nobody talks about. Let's break it down instantly.",
            "If you thought you knew everything about {topic}, think again. The latest trends show an unprecedented surge in demand for this exact insight.",
        ],
        "ctas": [
            "Share this with someone who needs to see it, and drop a comment below!",
            "Hit follow for daily exclusive breakdowns!",
            "Save this post so you don't lose it!",
        ],
    },
    "fr": {
        "hooks": [
            "Ce que personne ne vous dit sur {topic} va vous choquer !",
            "Tout ce que vous savez sur {topic} est complètement faux.",
            "Ce secret sur {topic} est en train de tout changer.",
        ],
        "bodies": [
            "Les récentes avancées dans le domaine de {topic} ont complètement transformé le paysage mondial. Voici ce que vous devez absolument savoir.",
            "La plupart des gens ignorent la vraie puissance de {topic}. Analysons ensemble les détails cachés qui font toute la différence.",
        ],
        "ctas": [
            "Partagez cette vidéo et donnez votre avis en commentaire !",
            "Abonnez-vous pour plus de contenuexclusif !",
        ],
    },
    "es": {
        "hooks": [
            "¡Lo que nadie te cuenta sobre {topic} te va a sorprender!",
            "Todo lo que sabías sobre {topic} es completamente falso.",
            "Este secreto sobre {topic} está cambiando las reglas del juego.",
        ],
        "bodies": [
            "Los recientes avances en {topic} han transformado por completo el panorama actual. Aquí tienes los detalles clave que necesitas saber ahora mismo.",
            "La mayoría de la gente ignora el verdadero impacto de {topic}. Vamos a desglosarlo paso a paso.",
        ],
        "ctas": [
            "¡Comparte este video y déjanos tu opinión en los comentarios!",
            "¡Sígueme para más contenido exclusivo!",
        ],
    },
    "zh": {
        "hooks": [
            "关于 {topic}， 99%的人不知道的惊天真相！",
            "彻底颠覆你认知的 {topic} 秘密来了！",
            "为什么大家都在偷偷关注 {topic} 的这个变化？",
        ],
        "bodies": [
            "近期在 {topic} 领域发生的巨变正在影响全球。如果你还不知道这些细节，就会错过 huge 机会。让我们一探究竟。",
            "很多人没有看透 {topic} 的本质。真正核心的秘密其实隐藏在日常的细节中，今天为你全面解析。",
        ],
        "ctas": [
            "快分享给你的好友，并在评论区留下你的看法！",
            "点击关注，获取更多独家硬核内容！",
        ],
    },
    "ja": {
        "hooks": [
            "{topic}について誰も教えてくれない衝撃の真実！",
            "これまでの{topic}の常識が180度変わります。",
            "今すぐ知るべき{topic}の隠された秘密とは？",
        ],
        "bodies": [
            "{topic}に関する最近の急激な変化は、世界中に大きな影響を与えています。見逃せない重要ポイントを分かりやすく解説します。",
            "多くの人が見落としている{topic}の本質。成功するための秘訣を今すぐチェックしましょう。",
        ],
        "ctas": [
            "ぜひシェアして、コメントであなたの意見を教えてください！",
            "フォローして最新の情報を手に入れよう！",
        ],
    },
}


def generate_unique_script(lang, topic):
  # إذا كانت اللغة موجودة في القوالب المتقدمة، ندمجها عشوائياً لمنع التكرار
  if lang in DYNAMIC_TEMPLATES:
    t = DYNAMIC_TEMPLATES[lang]
    hook = random.choice(t["hooks"]).format(topic=topic)
    body = random.choice(t["bodies"]).replace("{topic}", topic)
    cta = random.choice(t["ctas"])
    script = f"{hook}\n\n{body}\n\n{cta}"
  else:
    # لغات أخرى (دعم تلقائي عام)
    script = (
        f"Dynamic engaging breakdown and viral storytelling script about"
        f" '{topic}' optimized for local culture and maximum retention in"
        " language code: {lang}."
    )

  hashtags = (
      f"#{topic.replace(' ', '')} #Viral #ForYou #{lang.upper()} #Trending"
  )
  return script, hashtags


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مصنع المحتوى العالمي الذكي والمستقل</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; direction: rtl; }
        .container { max-width: 650px; margin: 0 auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
        h2 { color: #4CAF50; text-align: center; margin-bottom: 20px; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #b0bec5; }
        select, input[type="text"] { width: 100%; padding: 12px; margin-top: 8px; background: #2d2d2d; color: #fff; border: 1px solid #444; border-radius: 6px; font-size: 14px; }
        button { background: #4CAF50; color: white; border: none; padding: 14px 20px; margin-top: 25px; width: 100%; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #45a049; }
        #result { margin-top: 25px; background: #252525; padding: 20px; border-radius: 8px; white-space: pre-wrap; border-right: 5px solid #4CAF50; line-height: 1.6; font-size: 14px; }
        .section-title { color: #81c784; font-weight: bold; margin-top: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h2>مصنع المحتوى العالمي الذكي 🌍</h2>
        <form id="contentForm">
            <label for="topic">موضوع الفيديو أو الفكرة العامة:</label>
            <input type="text" id="topic" name="topic" placeholder="مثال: أسرار الذكاء الاصطناعي الخفية" required>
            
            <label for="lang">اختر لغة الدولة المستهدفة:</label>
            <select id="lang" name="lang">
                {% for code, name in languages.items() %}
                <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
            </select>
            
            <button type="button" onclick="generateContent()">توليد سيناريو فريد ومتجدد الآن</button>
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
            resultDiv.innerHTML = '🔄 جاري توليد سيناريو فريد ومتجدد باللغة المطلوبة...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: topic, lang: lang })
                });
                const data = await response.json();
                if(data.success) {
                    resultDiv.innerHTML = `
                        📚 <span class="section-title">اللغة المستهدفة:</span> ${data.selected_language_name}<br>
                        🎯 <span class="section-title">الموضوع الأساسي:</span> ${data.topic}<br><br>
                        ✍️ <span class="section-title">السيناريو الفريد والمتجدد (جاهز للنشر):</span><br>${data.script}<br><br>
                        🏷️ <span class="section-title">الكلمات المفتاحية والهاشتاغات:</span><br>${data.hashtags}<br><br>
                        🚀 <span class="section-title">المنصات الجاهزة:</span> ${data.platforms_ready.join(', ')}
                    `;
                } else {
                    resultDiv.innerHTML = '❌ حدث خطأ أثناء التوليد.';
                }
            } catch (error) {
                resultDiv.innerHTML = '❌ خطأ في الاتصال بالخادم.';
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(HTML_TEMPLATE, languages=WORLD_LANGUAGES)


@app.route("/generate", methods=["POST"])
def generate_global_content():
  data = request.json or {}
  lang = data.get("lang", "ar")
  topic = data.get("topic", "Technology")

  if lang not in WORLD_LANGUAGES:
    return jsonify({"error": "Language not supported"}), 400

  lang_name = WORLD_LANGUAGES[lang]
  script_text, hashtags = generate_unique_script(lang, topic)

  return jsonify({
      "success": true,
      "selected_language_code": lang,
      "selected_language_name": lang_name,
      "topic": topic,
      "script": script_text,
      "hashtags": hashtags,
      "platforms_ready": ["TikTok", "Instagram Reels", "YouTube Shorts"],
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
