import openai
from google.cloud import language_v1


def sentiment_score(text):
    client = language_v1.LanguageServiceClient()
    # Google Cloud Natural Language API를 사용하여 감정 점수 판단
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return sentiment.score


def refine_text(text):
    # 만약 텍스트가 부정적이라면, openai에게 어조를 개선하도록 요청합니다.
    system_prompt = f'''
            주어진 문장을 존댓말과 욕설을 제거하고, 순화한 문장으로 바꿔주세요.

            원래 말투: "{text}"
            순화된 말투:'''

    # OpenAI API를 호출하여 어조를 개선합니다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )

    refined_text = response.choices[0].message.content.strip()
    return refined_text

    
# main일 때
if __name__ == "__main__":
    text_to_refine = "씨발 어이가 없네"
    refined_text, sentiment_score = refine_text(text_to_refine)
    print("Original Text:", text_to_refine)
    print("Refined Text:", refined_text)
    print("Sentiment Score:", sentiment_score)
