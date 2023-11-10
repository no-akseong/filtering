from typing import Any

from langchain.tools import BaseTool
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import DuckDuckGoSearchResults
from langchain.utilities import DuckDuckGoSearchAPIWrapper


class SearchTool(BaseTool):
    name = "Search"
    description = "Useful for when you need to answer questions about ETRI(한국전자통신연구원) related things"

    wrapper = DuckDuckGoSearchAPIWrapper(region="kr-kr", time="y2", max_results=5)
    search_engine = DuckDuckGoSearchResults(api_wrapper=wrapper)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(self, query: str):
        return self.search_engine.run(query)

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
