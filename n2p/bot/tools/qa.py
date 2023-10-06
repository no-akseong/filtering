from typing import Any

from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from langchain.vectorstores import Chroma

import n2p.utils as utils
from n2p.utils import i, d
import val
import os

os.environ["OPENAI_API_KEY"] = val.OPENAI_API_KEY

qa_chain = None


def get_qa_chain():
    global qa_chain
    if qa_chain is None:
        qa_chain = create_qa_chain()
    return qa_chain


def create_qa_chain():
    # encoding 자동 감지
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(
        val.RES_DOCS_DIR,
        glob="./*.md",
        loader_cls=TextLoader,
        loader_kwargs=text_loader_kwargs,
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # persist_directory = val.DOCS_VECTOR_DB_DIR
    embedding = OpenAIEmbeddings()

    persist_directory = val.DOCS_VECTOR_DB_DIR
    # vector db가 없으면 embeddings 생성 후 저장
    if utils.is_empty_dir(persist_directory):
        i("vector db 생성중...")
        # 텍스트 임베딩 후 저장
        vectordb = Chroma.from_documents(documents=texts,
                                         embedding=embedding,
                                         persist_directory=persist_directory)
        vectordb.persist()
        vectordb = None

    # 저장되어있는 vector db 불러오기
    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)
    i("vector db 불러오는중...")

    # 검색기 생성 (search_kwargs: 참조 문서 개수)
    retriever = vectordb.as_retriever(search_kwargs={"k": 1})

    # chain 생성
    retrieval_qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),  # 단순 completion
        chain_type="stuff",
        retriever=retriever,
    )
    return retrieval_qa_chain


class QATool(BaseTool):
    name = "Retrieval QA"
    description = "Useful for when you need to answer questions about school related things."

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(self, query: str):
        return get_qa_chain().run(query)

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")

    def details(self, llm_response):
        print(llm_response["result"])
        print("\n\nSources:")
        for source in llm_response["source_documents"]:
            print(source.metadata["source"])


# main
if __name__ == "__main__":
    print("hi")