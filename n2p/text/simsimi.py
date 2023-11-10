import requests
import val

def bad_score(sentence):
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
    response = response.json()
    return response['bad'] if response['status'] == 200 else -1

# main
if __name__ == "__main__":
    print(bad_score("ㅅㅂ"))
