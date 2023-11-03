import urllib3
import json
import requests
import val


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

                # KoGPT에 설명 생성을 위한 프롬프트 생성
                prompt = f"{user_question}에 대한 답변은 다음과 같습니다: {answer}"
                kogpt_response = self.kogpt_api(prompt, max_tokens=32, temperature=0.7, top_p=1.0, n=3)
                kogpt_answer=kogpt_response['generations']
                return answer, kogpt_answer
            else:
                return "질문에 대한 답변을 찾을 수 없습니다.", None
        else:
            return "질문에 대한 답변을 찾을 수 없습니다.", None

if __name__ == "__main__":

    qa_system = QAWithKogptAndETRI(val.REST_API_KEY, val.ETRI_ACCESS_KEY,val.ETRI_DOC_KEY)

    user_question = input("질문을 입력하세요: ")

    answer, explanation = qa_system.generate_answer_and_explanation(user_question)

    print("답변:", answer)

    if explanation:
        print("KoGPT 설명:", explanation)
