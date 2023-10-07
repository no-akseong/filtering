import os
from os.path import join, abspath, dirname, sep

# 설정값
PROJECT_NAME = "n2p"
LOG_LEVEL = "d"
PORT = 11110

# 루트
ROOT_DIR = os.path.dirname(abspath(__file__))

# log
LOG_DIR = join(ROOT_DIR, "logs")

# api 키
OPENAI_API_KEY_FILE = join(ROOT_DIR, "openai_api_key.txt")
OPENAI_API_KEY = open(OPENAI_API_KEY_FILE).read()
GOOGLE_CLOUD_API_KEY = join(ROOT_DIR, r"spheric-bloom-400505-835efbd95c3c.json")
REST_API_KEY = join(ROOT_DIR, r"rest_api_key.txt")

# 리소스
RES_DIR = join(ROOT_DIR, "res")
RES_DOCS_DIR = join(RES_DIR, "docs")

DATA_DIR = join(ROOT_DIR, "data")
CONVERSATIONS_DIR = join(DATA_DIR, "conversations")
DOCS_VECTOR_DB_DIR = join(DATA_DIR, "docs_vector_db")
