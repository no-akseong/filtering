from google.cloud import vision


def detect_image_obscenity(img, is_file=False):
    """
    Google Cloud Vision API를 사용하여 이미지의 혐오 점수를 감지하고 유해 여부를 출력합니다.

    :param img: base64의 헤더를 제외한 데이터 부분만 입력
    """
    client = vision.ImageAnnotatorClient()

    if is_file:
        with open(img, "rb") as image_file:
            content = image_file.read()
    else:
        content = img

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    # 혐오 점수
    adult_likelihood = safe_search.adult.value
    medical_likelihood = safe_search.medical.value
    spoof_likelihood = safe_search.spoof.value
    violence_likelihood = safe_search.violence.value
    racy_likelihood = safe_search.racy.value

    # 결과 반환
    return {
        "adult": adult_likelihood,
        "medical": medical_likelihood,
        "spoof": spoof_likelihood,
        "violence": violence_likelihood,
        "racy": racy_likelihood,
    }


if __name__ == "__main__":
    import app
    app.setup()
    # 이미지 혐오 점수 및 유해 여부 감지 함수 호출 예제
    image_path = r"hit.jpeg"
    result = detect_image_obscenity(image_path, True)

    # 결과 출력
    print("Image Obscenity Scores:")
    print(f"Adult: {result['adult']}")  # 성인
    print(f"Medical: {result['medical']}")  # 약물
    print(f"Spoof: {result['spoof']}")  # 사기
    print(f"Violence: {result['violence']}")  # 폭력
    print(f"Racy: {result['racy']}")  # 선정
