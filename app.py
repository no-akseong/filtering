import os
from flask_socketio import SocketIO

from flask import Flask, send_file, request, jsonify

import n2p.utils as utils
import val
from n2p.bot.agent import agent
from n2p.bot.taskanal_agent import taskanal_agent
from n2p.img import face_blur
from n2p.img.google_img import detect_image_obscenity
from n2p.text.openai import refine_text
from n2p.text.google_nl import sentiment_score
from n2p.text.qanal import qanal
from n2p.utils import i, d
from n2p.text.simsimi import bad_score

app = Flask(__name__)
socketio = SocketIO(app)

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
    # streaming = data.get('streaming', False)
    # if streaming:
    #     pass
    # else:
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
    google_score = sentiment_score(user_msg)
    simsimi_score = bad_score(user_msg)

    response = {"google_score": google_score, "simsimi_score": simsimi_score}
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


@app.route('/img_obscenity', methods=['POST'])
def img_obscenity():
    """
    이미지의 혐오 점수를 감지하고 유해 여부를 출력합니다.
    이미지 형식: base64
    """
    data = request.get_json()
    image = data['img']

    # base64 encoding에서 data 추출
    image = image.split(',')[1]

    # 이미지 detect_image_obscenity() 함수로 전달
    scores = detect_image_obscenity(image)
    d(scores)
    # 스코어 반환
    return jsonify(scores), 200

@app.route('/blur_faces', methods=['POST'])
def blur_faces():
    """
    얼굴을 블러 처리합니다.
    이미지 형식: base64
    """
    data = request.get_json()
    image = data['img']
    # base64 encoding인 image_data에서 format을 추출
    header, encoded = image.split(",", 1)
    _, format = header.split(";")[0].split(":")[1].split("/")
    print("img_format", format)

    img_data = image.split(",")[1]

    # blur_faces() 함수로 전달
    blurred_image = face_blur.blur_faces(img_data, format)
    response = {"img": blurred_image}

    # 블러 처리된 이미지 반환
    return jsonify(response), 200

@app.route('/qanal', methods=['POST'])
def on_qanal():
    """
    고객의 질문을 분석합니다
    """
    data = request.get_json()
    question = data['q']
    response = qanal(question)

    # 블러 처리된 이미지 반환
    return jsonify(response), 200

@app.route('/taskanal', methods=['POST'])
def taskanal():
    """
    고객의 질문이 어떤 부서로 연결되어야 하는지 분석합니다 (연락처가 반환됨)
    """
    data = request.get_json()
    text = data['text']
    response = {'contact': taskanal_bot(text)['output']}


    # 블러 처리된 이미지 반환
    return jsonify(response), 200


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
        val.RES_TASKDOCS_DIR,
        val.DATA_DIR,
        val.CONVERSATIONS_DIR,
        val.DOCS_VECTOR_DB_DIR,
        val.RES_HWP_DIR,
        val.TASKANAL_DB_DIR
    ]

    # 폴더 생성
    for directory in dirs:
        utils.mkdirs(directory)


if __name__ == '__main__':
    setup()
    # 챗봇 생성
    chatbot = agent()
    taskanal_bot = taskanal_agent()

    i(f"서버가 {val.PORT}포트에서 시작됩니다.")
    app.run(debug=True, host='0.0.0.0', port=val.PORT)
    socketio.run(app, port=22221)
    i(f"서버 종료됨")
