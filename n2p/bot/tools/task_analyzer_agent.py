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

class StreamHandler(BaseCallbackHandler):
    def __init__(self, stream_callback):
        self.stream_callback = stream_callback

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.stream_callback(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        self.stream_callback("#END#")


def agent(stream_callback=None):
    # 현재 년도
    year = time.localtime().tm_year
    os.environ['OPENAI_API_KEY'] = val.OPENAI_API_KEY
    llm = ChatOpenAI(temperature=0, callbacks=[StreamHandler(stream_callback)])
    tools = [school_qa, calculator, task_analyzer]

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
        memory=memory
    )

    # If Assistant can't find the answer using search tool and there're some links to get access, Assistant should use "get_webpage" tool to get the webpage content.
    fixed_prompt = f'''Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant doesn't know anything about school related things so, should use some tools for questions about these topics. 
    Assistant should use "Task Tree" tool to find department contact number and must return the number only without any words.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    Assistant should answer in Korean. Please answer with nice words and polite words.

    Current year is {year}.
    '''

    conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = fixed_prompt
    return conversational_agent


if __name__ == '__main__':
    import app
    app.setup()
    chatbot = agent()
    # msg = chatbot("학생부좀 연결해 주세요")
    msg = chatbot("23만원을 12개월 내면 총 얼마죠?")
    print(f"챗봇: {msg['output']}")