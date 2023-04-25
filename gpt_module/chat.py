# -*- coding: utf-8 -*-
import os
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from api_keys import ApiKeys
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.utilities import (
    OpenWeatherMapAPIWrapper,
    WolframAlphaAPIWrapper,
    PythonREPL,
    WikipediaAPIWrapper
)
from custom_tools import TemperatureHumiditySensor, RainSensor
api = ApiKeys()
api.set_all_keys_as_env_vars()

search = SerpAPIWrapper()
weather = OpenWeatherMapAPIWrapper()
wolframalpha = WolframAlphaAPIWrapper()
pythonREPL = PythonREPL()
wikipedia = WikipediaAPIWrapper()
# temperatureHumidity = TemperatureHumiditySensor()
rainSensor = RainSensor()

tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="当你需要回答有关当前事件或世界现状的问题时请使用该工具"
    ),
    Tool(
        name="Weather",
        func=weather.run,
        description='''在你需要回答关于当前天气的问题时使用该工具。如果主人没有指定一个地点，你需要传入 "Nanjing,CN" 作为action_input''',
    ),
    Tool(
        name="Wolfram",
        func=wolframalpha.run,
        description="当你需要解决一些数学问题时请使用该工具，同时你必须将问题转化为数学语言。",
    ),
    Tool(
        name="PythonREPL",
        func=pythonREPL.run,
        description="你可以编写Python代码并执行它。例如，如果你想知道系统时间，你可以将相关Python代码传递给它，以获得当前的系统时间。"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="这是维基百科的api，如果你觉得需要使用维基百科请使用这个工具。"
    ),
    # Tool(
    #     name="RoomTempratureHumidity",
    #     func=temperatureHumidity(),
    #     description="如果你要知道房间内的温度和湿度请使用这个工具"
    # ),
    RainSensor()
]


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


llm = PromptLayerChatOpenAI(pl_tags=["langchain"],callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),verbose=True,streaming=True,temperature=0.9)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  memory=memory)

agent_chain.run(input="你好")
agent_chain.run(input="现在的美国总统是谁？")
agent_chain.run(input="sqrt(12)=?")
agent_chain.run(input="韦达定理是什么？")
agent_chain.run(input="现在天气如何？")
