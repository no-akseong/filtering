# import speech_recognition as sr


# # 음성 인식을 위한 recognizer 객체 생성
# r = sr.Recognizer()

# # 마이크로폰에서 음성을 입력받아 변환하는 함수
# def process_audio():
#     with sr.Microphone() as source:
#         print("음성 입력 대기 중...")
#         audio = r.listen(source)
        
#     try:
#         text = r.recognize_google_cloud(audio) # Google Cloud Speech-to-Text API를 사용하여 음성을 텍스트로 변환
#         print("음성 변환 결과:", text)
#     except sr.UnknownValueError:
#         print("음성을 인식할 수 없습니다.")
#     except sr.RequestError as e:
#         print("에러 발생:", str(e))

# # 코드 실행
# while True:
#     process_audio()

import speech_recognition as sr

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\gram\Desktop\project\fiitering\filltering\spheric-bloom-400505-835efbd95c3c.json'

r=sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio=r.listen(source)


    try:
        transcript=r.recognize_google(audio, language="ko-KR")
        print("Google Speech Recognition thinks you said "+transcript)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))