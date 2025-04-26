# backend/routes/quiz.py
from flask import Blueprint, request, jsonify
import requests
import os

quiz_bp = Blueprint('quiz', __name__)

# Utilise ta clé DeepSeek
DEEPSEEK_API_KEY = "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"
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@quiz_bp.route('/api/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    revision_content = data.get('content')
    
    if not revision_content:
        return jsonify({"error": "No revision content provided"}), 400

    prompt = f"Generate a multiple-choice question based on the following content:\n\n{revision_content}\n\nFormat it like:\nQuestion: ...\nA) ...\nB) ...\nC) ...\nAnswer: ..."

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 400
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "DeepSeek API error", "details": response.text}), 500

    try:
        result = response.json()
        raw_content = result['choices'][0]['message']['content']

        # Parser proprement
        parsed_quiz = parse_deepseek_response(raw_content)
        return jsonify(parsed_quiz)
    except Exception as e:
        return jsonify({"error": "Parsing failed", "details": str(e)}), 500

def parse_deepseek_response(raw_text):
    lines = raw_text.strip().split('\n')
    question = lines[0].replace('Question:', '').strip()
    options = []
    answer = ''

    for line in lines[1:]:
        if line.startswith(('A)', 'B)', 'C)', 'D)')):
            label, text = line.split(')', 1)
            options.append({"label": label.strip(), "text": text.strip()})
        elif line.startswith('Answer:'):
            answer = line.split(':', 1)[1].strip()

    return {
        "question": question,
        "options": options,
        "correct_answer": answer
    }
