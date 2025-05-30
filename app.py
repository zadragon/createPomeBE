from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://create-pome.vercel.app"}})


def get_emotions(text):
    prompt = f"""
다음 문장에서 느껴지는 감정을 가능한 한 풍부하고 구체하게 분석해줘.
감정 이름만, 쉼표로 구분해서 2~5개 정도로 써줘.

문장: "{text}"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def generate_poem(emotions):
    prompt = f"""
다음 감정들을 주제로 짧은 시 한 편을 써줘. 시는 자유시 형식으로, 4~6줄 정도로 써줘.
감정: {emotions}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

def generate_poem_with_title(emotions):
    prompt = f"""
다음 감정들을 바탕으로 시의 제목과 본문을 함께 써줘.

- 제목은 한 줄, 감정을 함축적으로 표현한 문장
- 시는 자유시 형식으로 4~6줄 정도
- 제목과 본문을 구분해서 써줘 (예: [제목] / [본문])

감정: {emotions}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()


@app.route("/poem", methods=["POST"])
def poem():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "텍스트가 없습니다"}), 400

    try:
        emotions = get_emotions(text)
        poem_with_title = generate_poem_with_title(emotions)
        return jsonify({
            "emotions": emotions,
            "poem": poem_with_title
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
