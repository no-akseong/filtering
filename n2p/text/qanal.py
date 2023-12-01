import val
import urllib3
import json

def qanal(question):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseQAnal"
    accessKey = val.ETRI_ACCESS_KEY

    requestJson = {
        "argument": {
            "text": question
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    # print(response.data)
    response_data = json.loads(response.data.decode('utf-8'))
    return response_data

def extract_category(result):
    """
    ETRI의 WiseQAnal API를 통해 분석된 결과에서 가장 높은 확률의 카테고리를 추출
    :param result: WiseQAnal API의 분석 결과 (json)
    """
    vSATs_list = result['return_object']['orgQInfo']['orgQUnit']['vSATs']

    # 'dConfidenceSAT'를 기준으로 내림차순 정렬
    sorted_vSATs = sorted(vSATs_list, key=lambda x: x['dConfidenceSAT'], reverse=True)

    # 결과 출력
    category = sorted_vSATs[0]['strSAT']
    return category

# main
if __name__ == '__main__':
    import app
    app.setup()
    question = "초등학교 장학 관련은 어디에다 전화해야 하나요?" # OGG_EDUCATION
    # question = "정부기관 교통 관련은 어디에다 전화해야 하나요?" # OGG_POLITICS
    r = qanal(question)
    print(r)
    print(extract_category(r))

