import os

import openai
from flask import Flask, send_file, request, jsonify
from google.cloud import language_v1

import n2p.utils as utils
import val
from n2p.bot.agent import agent
from n2p.img.safe_search import detect_image_obscenity
from n2p.text.chat_gpt import sentiment_score, refine_text
from n2p.utils import i, d

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    요청이 들어오면 챗봇이 적절한 답변을 보냅니다.
    """
    data = request.get_json()
    d(f"/chat: {data}")

    # 사용자가 보낸 메시지
    user_msg = data['text']
    msg = chatbot(user_msg)['output']

    response = {"text": msg}
    return jsonify(response), 200


@app.route('/sentiment', methods=['POST'])
def check_sentiment():
    """
    문장의 감정 점수를 분석해줍니다.
    """
    data = request.get_json()
    d(f"/check_sentiment: {data}")

    # 사용자가 보낸 메시지
    user_msg = data['text']

    # 감정 점수 계산
    score = sentiment_score(user_msg)

    response = {"score": score}
    return jsonify(response), 200


# 문장을 정제해 줍니다
@app.route('/refine_text', methods=['POST'])
def on_refine_text():
    """
    문장을 정제해줍니다.
    """
    data = request.get_json()
    d(f"/refine_text: {data}")

    # 사용자가 보낸 메시지
    user_msg = data['text']

    # refined_text 맨 앞과 맨 뒤 " 제거
    refined_text = refine_text(user_msg)[1:-1]
    response = {"refined_text": refined_text}
    return jsonify(response), 200


@app.route('/safe_img', methods=['POST'])
def safe_img():
    if 'image' not in request.files:
        return

    image = request.files['image']

    # 이미지 detect_image_obscenity() 함수로 전달
    is_safe = detect_image_obscenity(image)
    return jsonify(is_safe), 200


def setup():
    # OpenAI API 키 설정
    os.environ['OPENAI_API_KEY'] = val.OPENAI_API_KEY
    # Google Cloud Natural Language API 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = val.GOOGLE_CLOUD_API_KEY

    # 생성해야 할 폴더 리스트
    dirs = [
        val.LOG_DIR,
        val.RES_DIR,
        val.RES_DOCS_DIR,
        val.DATA_DIR,
        val.CONVERSATIONS_DIR,
        val.DOCS_VECTOR_DB_DIR,
    ]

    # 폴더 생성
    for directory in dirs:
        utils.mkdirs(directory)


if __name__ == '__main__':
    setup()
    # 챗봇 생성
    chatbot = agent()

    i(f"서버가 {val.PORT}포트에서 시작됩니다.")
    app.run(debug=True, host='0.0.0.0', port=val.PORT)
    i(f"서버 종료됨")
