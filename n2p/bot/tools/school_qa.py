from typing import Any

from langchain.tools import BaseTool

import val
from n2p.bot.tools.qa_chain import get_qa_chain
from n2p.text.ETRI_qa import docqa


class SchoolQATool(BaseTool):
    """
    ETRI QA API 사용중
    """
    name = "School QA"
    description = "Useful for when you need to answer questions about school related things."

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(self, query: str):
        return docqa(query, val.ETRI_SCHOOL_DOC_ID)

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")

    def details(self, llm_response):
        print(llm_response["result"])
        print("\n\nSources:")
        for source in llm_response["source_documents"]:
            print(source.metadata["source"])


# main
if __name__ == "__main__":
    print(get_qa_chain().run("한국초등학교 전화번호 알려줘"))
