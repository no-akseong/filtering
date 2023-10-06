import os
from google.cloud import vision

# JSON 키 파일의 경로 설정
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\gram\Desktop\project\positive-word\spheric-bloom-400505-835efbd95c3c.json'


def detect_image_obscenity(image_path):
    """Google Cloud Vision API를 사용하여 이미지의 혐오 점수를 감지하고 유해 여부를 출력합니다."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    # 혐오 점수
    adult_likelihood = safe_search.adult
    medical_likelihood = safe_search.medical
    spoof_likelihood = safe_search.spoof
    violence_likelihood = safe_search.violence
    racy_likelihood = safe_search.racy

    # 혐오 점수가 "LIKELY" 또는 "VERY_LIKELY"인 경우 이미지를 유해하다고 판단
    harmful = (adult_likelihood >= 4 or medical_likelihood >= 4 or spoof_likelihood >= 4 or
               violence_likelihood >= 3 or racy_likelihood >= 3)

    # 결과 반환
    return {
        "adult": adult_likelihood,
        "medical": medical_likelihood,
        "spoof": spoof_likelihood,
        "violence": violence_likelihood,
        "racy": racy_likelihood,
        "harmful": harmful,
    }


if __name__ == "__main__":
    # 이미지 혐오 점수 및 유해 여부 감지 함수 호출 예제
    image_path = r"C:\Users\gram\Downloads\42933324-폭력적인-아버지는-가족의-대-히트.jpg"
    result = detect_image_obscenity(image_path)

    # 결과 출력
    print("Image Obscenity Scores:")
    print(f"Adult: {result['adult']}")  # 성인
    print(f"Medical: {result['medical']}")  # 약물
    print(f"Spoof: {result['spoof']}")  # 사기
    print(f"Violence: {result['violence']}")  # 폭력
    print(f"Racy: {result['racy']}")  # 선정

    print("Image Harmful: ", result['harmful'])
