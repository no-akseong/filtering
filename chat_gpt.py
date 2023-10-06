import openai
from google.cloud import language_v1
import os

def refine_tone_with_openai(text_to_refine, google_cloud_key, openai_api_key):
    # Google Cloud Natural Language API 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_cloud_key
    client = language_v1.LanguageServiceClient()

    # OpenAI 설정
    openai.api_key = openai_api_key

    # Google Cloud Natural Language API를 사용하여 감정 점수 판단
    document = language_v1.Document(content=text_to_refine, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # 감정 점수를 기준으로 텍스트가 부정적인지 판단합니다.
    negative_threshold = -0.2
    is_negative = sentiment.score < negative_threshold

    if is_negative:
        # 만약 텍스트가 부정적이라면, openai에게 어조를 개선하도록 요청합니다.
        prompt = f'''
        주어진 문장을 존댓말과 욕설을 제거하고, 순화한 문장으로 바꿔주세요.

        원래 말투: "{text_to_refine}"
        순화된 말투:'''

        # OpenAI API를 호출하여 어조를 개선합니다.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "넌 챗봇이야."},
                {"role": "user", "content": prompt}
            ]
        )

        refined_text = response.choices[0].message.content.strip()

        # 감정 점수와 함께 반환합니다.
        return refined_text, sentiment.score
    else:
        # 만약 텍스트가 부정적이지 않다면 원본 텍스트와 감정 점수를 반환합니다.
        return text_to_refine, sentiment.score
    

# 사용 예제
# Google Cloud 서비스 계정 키 읽기
google_cloud_key = r'C:\Users\gram\Desktop\project\positive-word\spheric-bloom-400505-835efbd95c3c.json'

# OpenAI API 키 읽기
with open(r'C:\Users\gram\Desktop\project\positive-word\openai_api_key.txt', 'r') as key_file:
    openai_api_key = key_file.read()

text_to_refine = "씨발 어이가 없네"
refined_text, sentiment_score = refine_tone_with_openai(text_to_refine, google_cloud_key, openai_api_key)
print("Original Text:", text_to_refine)
print("Refined Text:", refined_text)
print("Sentiment Score:", sentiment_score)
