import urllib3
import json
import requests
import val
import os


class QAWithKogptAndETRI:
    def __init__(self, kogpt_rest_api_key, etri_access_key, etri_doc_key):
        self.kogpt_rest_api_key = kogpt_rest_api_key
        self.etri_access_key = etri_access_key
        self.etri_doc_key = etri_doc_key

    # KoGPT API 호출
    def kogpt_api(self, prompt, max_tokens=1, temperature=1.0, top_p=1.0, n=1):
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
                'Authorization': 'KakaoAK ' + self.kogpt_rest_api_key,
                'Content-Type': 'application/json'
            }
        )
        response = json.loads(r.content)
        return response

    # ETRI 문서 질의
    def etri_query_document(self, question):
        openApiURL = "http://aiopen.etri.re.kr:8000/DocQA"

        requestJson = {
            "argument": {
                "question": question,
                "doc_key": self.etri_doc_key
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": self.etri_access_key},
            body=json.dumps(requestJson)
        )

        response_data = json.loads(response.data.decode('utf-8'))
        return response_data

    # 질문에 대한 답변과 설명 생성
    def generate_answer_and_explanation(self, user_question):
        response_data = self.etri_query_document(user_question)

        if 'return_object' in response_data and 'DocInfo' in response_data['return_object']:
            doc_info = response_data['return_object']['DocInfo']
            if doc_info:
                answer = doc_info[0]['answer']
                return answer

                # KoGPT에 설명 생성을 위한 프롬프트 생성
                prompt = f"{user_question}에 대한 답변은 다음과 같습니다: {answer}"
                kogpt_response = self.kogpt_api(prompt, max_tokens=32, temperature=0.7, top_p=1.0, n=3)
                kogpt_answer=kogpt_response['generations']
                return answer, kogpt_answer
            else:
                return "질문에 대한 답변을 찾을 수 없습니다.", None
        else:
            return "질문에 대한 답변을 찾을 수 없습니다.", None



def upload_doc(file, format):
    # hwpx 오류나서 hwp로 변환 후 업로드
    openApiURL = "http://aiopen.etri.re.kr:8000/DocUpload"
    accessKey = val.ETRI_ACCESS_KEY
    uploadFilePath = os.path.join(val.RES_HWP_DIR, file)

    file = open(uploadFilePath, 'rb')
    fileContent = file.read()
    file.close()
    # {'result': '0', 'return_type': 'com.google.gson.internal.LinkedTreeMap', 'return_object': {'doc_key': '6f0052c3-fcc6-433f-a51c-65276633f2d8_AAEEF08E7F0001015D83C3F600017534'}, 'request_id': 'AAEEF08D7F0001015D83C3F60064321C'}
    requestJson = {
        "argument": {"type": format}
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Authorization": accessKey},
        fields={
            'json': json.dumps(requestJson),
            'doc_file': (os.path.basename(file.name), fileContent)
        }
    )

    response_data = json.loads(response.data.decode('utf-8'))
    return response_data['return_object']['doc_key']

def docqa(question, doc_key):
    openApiURL = "http://aiopen.etri.re.kr:8000/DocQA"
    accessKey = val.ETRI_ACCESS_KEY
    # doc_key = val.ETRI_SCHOOL_DOC_ID

    requestJson = {
        "argument": {
            "question": question,
            "doc_key": doc_key
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    response_data = json.loads(response.data.decode('utf-8'))
    # answer만 추출해서 return
    return response_data['return_object']['DocInfo'][0]['answer']

if __name__ == "__main__":

    # qa_system = QAWithKogptAndETRI(val.REST_API_KEY, val.ETRI_ACCESS_KEY, val.ETRI_DOC_KEY)
    #
    # qanal("제가 지금 교통사고가 났는데 교통부에 전화했는데 왜 아무런 조치가 없나요?")

    r = docqa("한국초등학교 전화번호", val.ETRI_SCHOOL_DOC_ID)
    print("결과:", r)

    # user_question = "언제까지 지원가능한가요?"
    #
    # answer = qa_system.generate_answer_and_explanation(user_question)
    #
    # print("답변:", answer)

    # if explanation:
    #     print("KoGPT 설명:", explanation)
