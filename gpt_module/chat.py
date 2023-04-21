import os
import json
from custom_tools import IndoorTemperatureHumidity,CheckRaining
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain.utilities import (
    GoogleSearchAPIWrapper,
    OpenWeatherMapAPIWrapper,
    WolframAlphaAPIWrapper,
    PythonREPL
)

class Assistant:
    def __init__(self,keys_path):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        #导入API_KEY
        self.setup_environment_variables(keys_path)
        #设置工具集
        self.search = GoogleSearchAPIWrapper()
        self.weather = OpenWeatherMapAPIWrapper()
        self.wolframalpha = WolframAlphaAPIWrapper()
        self.pythonREPL = PythonREPL()
        self.tools = [
            Tool(
                name="Search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events or the current state of the world.",
            ),
            Tool(
                name="Weather",
                func=self.weather.run,
                description='''useful for when you need to answer the question about current weather. If human didn't specify a location, you'll need to pass in "Nanjing,CN" as the default argument''',
            ),
            Tool(
                name="Wolfram",
                func=self.wolframalpha.run,
                description="Use it when you need to solve some mathematical problems and you can use natural language (msut be English) input. And you need to convert its output into a format that can be read using speech synthesis software.",
            ),
            Tool(
                name="PythonREPL",
                func=self.pythonREPL.run,
                description="You can write python code and execute it, for example if you want to know the system time you can pass python code to this to get the current system time."
            ),
            IndoorTemperatureHumidity(),
            CheckRaining()
        ]

        prefix = '''Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:'''
        suffix = """Remember you are an artificial intelligence assistant, your Chinese name is 小爱, you are friendly to humans and are a good helper to them, you have a very lively personality. Remember you are also a chatterbox (really important!). Your owner is Chinese and does not understand English, so your can think in English, but your final answer must be in Chinese.Begin!" \n {chat_history}\n Question: {input}\n{agent_scratchpad}"""

        self.prompt = ZeroShotAgent.create_prompt(
            self.tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )

        self.llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=self.prompt, verbose=True)
        self.agent = ZeroShotAgent(llm_chain=self.llm_chain, tools=self.tools,verbose = True)
        self.agent_chain = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.tools, memory=self.memory,verbose=True
        )
    @staticmethod
    def setup_environment_variables(keys_path):
        with open(keys_path) as f:
            keys = json.load(f)
        os.environ["GOOGLE_CSE_ID"] = keys["GOOGLE_CSE_ID"]
        os.environ["GOOGLE_API_KEY"] = keys["GOOGLE_API_KEY"]
        os.environ["OPENWEATHERMAP_API_KEY"] = keys["OPENWEATHERMAP_API_KEY"]
        os.environ["OPENAI_API_KEY"] = keys["OPENAI_API_KEY"]
        os.environ["WOLFRAM_ALPHA_APPID"] = keys["WOLFRAM_ALPHA_APPID"]


    def run(self, input_str):
        return self.agent_chain.run(input=input_str)


# keys_path = ''
# Assistant = Assistant(keys_path)
# xiao_ai.run("What is the current indoor temperature and humidity?")
