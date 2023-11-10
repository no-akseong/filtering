from google.cloud import language_v1

def sentiment_score(text):
    client = language_v1.LanguageServiceClient()
    # Google Cloud Natural Language API를 사용하여 감정 점수 판단
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return sentiment.score