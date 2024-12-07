from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from symptom_matcher import find_matching_diseases

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)

@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    target_langcode = data.get('language', 'en')

    if not message.strip():
        return jsonify({"error": "empty message box"}), 400

    response = find_matching_diseases(message, target_langcode)
    """
    return {
        "tokens": tokens,
        "top_matches_dict": top_matches_dict,
        "symptoms_in_english": symptoms_in_english,
        "detected_language": detected_language,
        "target_language" : target_language,
        "response_in_target_language": response_in_target_language,
    }
    """

    return jsonify({
            "tokens": response["tokens"],
            "translatedResponse": response["response_in_target_language"],
            "detectedLanguage": response["detected_language"],
            "targetLanguage": response["target_language"]
        })


if __name__ == '__main__':
    app.run(debug=True)