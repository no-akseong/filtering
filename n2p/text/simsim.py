import requests
import val

def simsimi(sentence):
    # 요청 헤더 및 본문 데이터 설정
    url = "https://wsapi.simsimi.com/190410/classify/bad"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": val.SIMSIMI_API_KEY
    }
    data = {
        "sentence": sentence,
        "lang": "ko",
        "type": "DPD"
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, json=data)

    # 응답 데이터를 JSON 형식으로 변환
    response = response.json()

    # 응답 출력
    # response 형식
    # {"status": 200, "statusMessage": "OK", "bad": 0.999804,
    # "request": {
    # "sentence": "ㅅㅂ", "lang": "ko"}
    # }
    if response['status'] == 200:
        return response['bad']
    else:
        return -1

# main
if __name__ == "__main__":
    print(simsimi("ㅅㅂ"))
