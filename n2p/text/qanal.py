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

    print(response.data)
    response_data = json.loads(response.data.decode('utf-8'))
    return response_data


# main
if __name__ == '__main__':
    import app
    app.setup()
    question = "코로나19는 어떻게 전파되나요?"
    print(qanal(question))