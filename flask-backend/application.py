from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from translation import *
from symptom_matcher import *

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
    target_language = data.get('language', 'en')

    if not message:
        return jsonify({"error": "empty message box"}), 400

    tokens               = tokenize(message)
    sentence_translation = translate_sentence(message, target_language)
    detected_language    = detect_language(message)

    return jsonify({
        "tokens": tokens,
        "sentence_translation": sentence_translation,
        "language_info": detected_language
    })

# Endpoint to handle symptom matching
@app.route('/symptom-checker', methods=['POST'])
def symptom_checker():
    """
    Endpoint to check symptoms and provide likely diseases.
    Input: JSON with a "symptoms" field.
    Output: JSON with top matching diseases and their similarity scores.
    """
    try:
        # Parse user input
        data = request.json
        user_symptoms = data.get('symptoms', '')

        if not user_symptoms.strip():
            return jsonify({"error": "No symptoms provided."}), 400

        # Find matching diseases
        matches = find_matching_diseases(user_symptoms, symptom_data)

        # Return the results
        return jsonify({"matches": matches}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
