import openai

def refine_text(text):
    # 만약 텍스트가 부정적이라면, openai에게 어조를 개선하도록 요청합니다.
    system_prompt = f'''주어진 문장에서 부정표현과 욕설을 제거하고, 
D순화한 문장으로 바꿔서 존댓말과 이쁜말로 만들어주세요.

밑의 백틱 3개로 감싼곳은 순화대화의 예시 대화입니다.
```
원래 말투: "이게 뭐야? 완전 별로잖아!"
순화된 말투: "이건 어때요? 아쉽네요."

원래 말투: "왜 이렇게 좇같이 만들었어?"
순화된 말투: "왜 이렇게 아쉽게 만들었나요?"

원래 말투: "이런 거 정말 좇같아."
순화된 말투: "이런 상황은 정말 힘드네요."

원래 말투: "왜 이딴 똘추 같은 짓을 했어?"
순화된 말투: "왜 이상한 행동을 했을까요?"
```

원래 말투:{text}
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
    import app
    app.setup()

    text_to_refine = "씨발 어이가 없네"
    refined_text, sentiment_score = refine_text(text_to_refine)
    print("Original Text:", text_to_refine)
    print("Refined Text:", refined_text)
    print("Sentiment Score:", sentiment_score)
