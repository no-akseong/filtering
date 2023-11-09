from typing import Any

from langchain.tools import BaseTool

class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "Useful for when you need to answer questions about calculations. Input must be a valid mathematical expression"

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(self, query: str):
        # calculate the query using eval()
        return eval(query)

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")

# main
if __name__ == "__main__":
    print(type(eval('1+3')))