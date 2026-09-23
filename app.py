from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Content Factory is running successfully!"
    })

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json or {}
    # يمكنك إضافة منطق توليد المحتوى هنا بكل سهولة
    return jsonify({
        "success": True,
        "content": "Sample generated content"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
