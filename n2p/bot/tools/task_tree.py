from typing import Any

from langchain.tools import BaseTool

from n2p.bot.tools.qa_chain import get_qa_chain


class TaskTreeTool(BaseTool):
    name = "Task Tree"
    description = "Useful for when you need to answer questions about selecting related task contacts."

    def __init__(self, **data: Any):
        # data['return_direct'] = True
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
    print(get_qa_chain().run("한국초등학교 전화번호 알려줘"))
