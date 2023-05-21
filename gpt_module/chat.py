# -*- coding: utf-8 -*-
import os
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.utilities import (
    SerpAPIWrapper,
    OpenWeatherMapAPIWrapper,
    WolframAlphaAPIWrapper,
    PythonREPL,
    WikipediaAPIWrapper
)
from langchain.chat_models import PromptLayerChatOpenAI
# from .api_keys import ApiKeys
# from .custom_tools import IndoorTemperatureHumidity, CheckRaining,TurnOnLight
from api_keys import ApiKeys
from custom_tools import IndoorTemperatureHumidity, CheckRaining,TurnOnLight

class LangChainAgent:
    def __init__(self):
        self.api = ApiKeys()
        self.api.set_all_keys_as_env_vars()

        self.search = SerpAPIWrapper()
        self.weather = OpenWeatherMapAPIWrapper()
        self.wolframalpha = WolframAlphaAPIWrapper()
        self.pythonREPL = PythonREPL()
        self.wikipedia = WikipediaAPIWrapper()

        self.tools = [
            Tool(
                name="Search",
                func=self.search.run,
                description="当你需要回答有关当前事件或世界现状的问题时请使用该工具"
            ),
            Tool(
                name="Weather",
                func=self.weather.run,
                description='''在你需要回答关于当前天气的问题时使用该工具。如果主人没有指定一个地点，你需要传入 "Nanjing,CN" 作为action_input''',
            ),
            Tool(
                name="Wolfram",
                func=self.wolframalpha.run,
                description="当你需要解决一些数学问题时请使用该工具，同时你必须将问题转化为数学语言。",
            ),
            IndoorTemperatureHumidity(),
            TurnOnLight()

        ]

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.llm = PromptLayerChatOpenAI(
            pl_tags=["langchain"],
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            verbose=True,
            streaming=True,
            temperature=0.9
        )

        self.agent_chain = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory
        )

    def response(self, message):
        return self.agent_chain.run(message)
    

if __name__ == "__main__":
    openai_chat_module = LangChainAgent()
    Question = "Question:打开室内的灯"
    print(Question)
    # resp = openai_chat_module.response("现在室内的温度湿度怎么样？")
    resp = openai_chat_module.response("现在的英国首相是谁?")
    # resp = openai_chat_module.response("打开室内的灯")
    # resp = openai_chat_module.response("今天天气怎么样？")
    print(resp)