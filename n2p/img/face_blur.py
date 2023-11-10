# -*- coding:utf-8 -*-
import base64
import json
from io import BytesIO

import cv2
import numpy as np
import urllib3
from PIL import Image

import val


def face_locs(img):
    """
    얼굴 위치를 찾아주는 함수
    :param img: 이미지 (base64 형식)
    """
    openApiURL = "http://aiopen.etri.re.kr:8000/FaceDeID"
    accessKey = val.ETRI_ACCESS_KEY
    type = "1"  # 얼굴 비식별화 기능 "1"로 설정
    requestJson = {
        "argument": {
            "type": type,
            "file": img
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    # 얼굴 위치 리스트
    locs = []
    # 얼굴 위치 리스트에 얼굴 위치 추가
    for face in json.loads(response.data.decode('utf-8'))['return_object']['results']:
        locs.append((face['x'], face['y'], face['width'], face['height']))
    return locs


def blur_faces(img_base64, format):
    """
    얼굴을 블러 처리합니다.
    :param img_base64: 이미지 (base64 형식, 앞의 header는 제외)
    :param format: 이미지 형식 (ex: png, jpeg)
    """
    # 얼굴 위치 리스트 가져오기
    faces = face_locs(img_base64)

    # 이미지를 OpenCV 형식으로 변환합니다. (블러 처리를 위해)
    image = base64_to_cv2(img_base64)

    # 인식된 얼굴 영역에 블러 처리를 적용합니다.
    for (x, y, w, h) in faces:
        face_roi = image[y:y + h, x:x + w]
        blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
        image[y:y + h, x:x + w] = blurred_face

    # 결과 이미지를 저장합니다.
    cv2.imwrite(f'blurred_faces.{format}', image)

    # 결과 이미지를 base64 형식으로 변환합니다.
    result = cv2_to_base64(image, format)
    return result


def base64_to_cv2(base64_image_string):
    print(base64_image_string[:30])
    # Base64 문자열을 디코딩하여 바이너리 데이터로 변환합니다.
    image_data = base64.b64decode(base64_image_string)

    # 바이너리 데이터로부터 PIL 이미지 객체를 생성합니다.
    image = Image.open(BytesIO(image_data))

    # PIL 이미지 객체를 OpenCV 이미지 객체로 변환합니다.
    open_cv_image = np.array(image)
    # 이 과정에서 RGB가 BGR로 변환됩니다. OpenCV는 BGR을 사용합니다.
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image

def cv2_to_base64(cv2_img, format):
    # 이미지를 메모리 버퍼에 PNG 형식으로 인코딩합니다.
    _, buffer = cv2.imencode(f'.{format}', cv2_img)

    # 메모리 버퍼의 바이트 데이터를 Base64 문자열로 인코딩합니다.
    base64_image_string = base64.b64encode(buffer).decode('utf-8')
    base64_image_string = f'data:image/{format};base64,{base64_image_string}'
    return base64_image_string

def raw_to_base64(img):
    # 이미지를 base64 형식으로 변환합니다.
    with open(img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# main
if __name__ == '__main__':
    img = 'ppl.jpeg'
    format = 'jpeg'
    img_base64 = raw_to_base64(img)
    blur_faces(img_base64, format)


