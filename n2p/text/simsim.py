import requests
import os

with open("C:/Users/gram/Desktop/project/fiitering/filltering/simsim_api_key.txt", "r") as key_file:
    api_key = key_file.read().strip()

# 요청 헤더 및 본문 데이터 설정
url = "https://wsapi.simsimi.com/190410/classify/bad"
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key
}
data = {
    "sentence": "너가 이렇게 하면 널 고소할 수도 있는데, 괜찮겠어?",
    "lang": "ko",
    "type": "DPD"
}

# POST 요청 보내기
response = requests.post(url, headers=headers, json=data)

# 응답 출력
print(response.status_code)  # 상태 코드
print(response.text)         # 응답 본문
