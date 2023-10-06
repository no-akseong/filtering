# 필요한 라이브러리 가져오기
from google.cloud import language_v1  # Google Cloud Natural Language API 사용을 위한 라이브러리
import os  # 환경 변수 설정을 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리
import json  # JSON 데이터 처리를 위한 라이브러리

# Google Cloud Natural Language API 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\gram\Desktop\project\fiitering\filltering\spheric-bloom-400505-835efbd95c3c.json'  # JSON 키 파일의 경로 설정
client = language_v1.LanguageServiceClient()  # Natural Language API 클라이언트 인스턴스 생성

# KoGPT API 설정

with open(r'C:\Users\gram\Desktop\project\fiitering\filltering\rest_api_key.txt', 'r') as key_file:
    REST_API_KEY = key_file.read()
  # KoGPT API의 인증 키

# KoGPT API를 호출하는 함수 정의
def kogpt_api(prompt, max_tokens=10, temperature=0.7, top_p=1.0, n=1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json={
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers={
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

# 텍스트 어조를 개선하는 함수 정의
def refine_tone(text):
    # Google Cloud Natural Language API를 사용하여 텍스트의 감정을 감지합니다.
    document = language_v1.types.Document(content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # 감정 점수를 기준으로 텍스트가 부정적인지 판단합니다. (이 점수 기준을 조절할 수 있습니다)
    negative_threshold = -0.2
    is_negative = sentiment.score < negative_threshold

    if is_negative:
        # 만약 텍스트가 부정적이라면, KoGPT에게 어조를 개선하도록 요청합니다.
        prompt = f'''주어진 문장을 존댓말과 욕설을 제거하고, 순화한 문장으로 바꿔주세요.

        원래 말투: "이게 뭐야? 완전 별로잖아!"
        순화된 말투: "이건 어때요? 아쉽네요."

        원래 말투: "그냥 이딴 거나 해!"
        순화된 말투: "그냥 다른 걸로 하죠."

        원래 말투: "왜 이렇게 좇같이 만들었어?"
        순화된 말투: "왜 이렇게 아쉽게 만들었나요?"

        원래 말투: "이 병신같은 일을 왜 했어?"
        순화된 말투: "이 이상한 일을 왜 했을까요?"

        원래 말투: "이게 뭐라고? 정말 이해 못하겠어!"
        순화된 말투: "이게 뭐라고요? 정말 이해하기 어려워요."

        원래 말투: "이런 거 정말 좇같아."
        순화된 말투: "이런 상황은 정말 귀찮아요."

        원래 말투: "왜 이딴 똘추 같은 짓을 했어?"
        순화된 말투: "왜 이상한 행동을 했을까요?"

        원래 말투: "나도 모르게 존나 화가 나!"
        순화된 말투: "나도 모르게 정말 답답해져요."

        원래 말투: "이게 어떻게 이렇게 엉망이야?"
        순화된 말투: "이게 어떻게 이렇게 복잡한 상태일까요?"

        원래 말투: "씨발 왜 이딴 걸 내 앞에 놓아 놨어?"
        순화된 말투: "왜 이런 것을 내 앞에 두셨나요?"

        원래 말투:{text}
        순화된 말투:'''
        response = kogpt_api(prompt, max_tokens=10, temperature=0.5)
        print(response['generations'])

        if 'generations' in response and response['generations']:
            refined_text = response['generations'][0]['text']
            return refined_text
        else:
            # 만약 KoGPT가 응답하지 않았다면 원본 텍스트를 반환합니다.
            return text
    else:
        # 만약 텍스트가 부정적이지 않다면 원본 텍스트를 반환합니다.
        return text

# main일 때
if __name__ == "__main__":
    # 예제 사용법
    text_to_refine = "어이가 없네"  # 이 문장을 부정적으로 설정하면 수정됩니다.
    refined_text = refine_tone(text_to_refine)
    print("Original Text:", text_to_refine)
    print("Refined Text:'", refined_text)

