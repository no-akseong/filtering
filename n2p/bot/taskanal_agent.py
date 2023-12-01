import os
from typing import Any

from langchain.agents import initialize_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult

from n2p.bot.tools import *
import val
import time
from n2p.utils import i, d

def taskanal_agent():
    os.environ['OPENAI_API_KEY'] = val.OPENAI_API_KEY
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    tools = []

    # conversational agent memory
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=3,
        return_messages=True
    )

    # create our agent
    conversational_agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=5,
        early_stopping_method='generate',
        memory=memory,
        handle_parsing_errors=True
    )

    # Assistant should use "Task Tree" tool to find department contact number.
    # If Assistant can't find the answer using search tool and there're some links to get access, Assistant should use "get_webpage" tool to get the webpage content.
    fixed_prompt = f'''Assistant is a large language model trained by OpenAI.

Assistant should return "department" only when user wants to contact a department.

Below is about each department.
```
# 교무부
- 역할: 교육과정 및 수업 관련 업무를 담당.
- 담당: 교사의 수업 시간표 작성, 학생 성적 관리, 교육 프로그램 개발 및 평가.

# 학생부
- 역할: 학생 지도 및 복지에 관련된 업무를 담당.
- 담당: 상담 활동, 출결 관리, 장학금 운영, 학생 생활지도.

# 입학부
- 역할: 신입생 선발 및 입학에 관련된 업무를 담당.
- 담당: 입학 시험 관리, 지원자 서류 검토, 신입생 등록 관리.
```

Following is an example conversation between a user and Assistant.
```
User: 입학관련해서 문의할려고 해요
Assistant: 입학부
User: 학생 성적관련해서 질문 할려고요
Assistant: 교무부
```

Do not use any other words except each department in the response.
'''

    conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt
    return conversational_agent


if __name__ == '__main__':
    import app
    app.setup()
    chatbot = taskanal_agent()
    # msg = chatbot("입학관련해서 문의할려고 해요")
    msg = chatbot("학생 성적표 관련해서 질문 할려고요")
    print(f"챗봇: {msg['output']}")
