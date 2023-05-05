# GPTSpeaker
嵌入式课程设计——基于ChatGPT的智能音箱


## 基本架构
![基本架构](./pic/%E9%A1%B9%E7%9B%AE%E6%A1%86%E6%9E%B6.png)


## 唤醒词检测
唤醒词是用于触发智能音箱后续功能的信号。  
解决方案：[picovoice]( https://picovoice.ai/)

## 语音识别
语音通过将声音信号转换成文本用于与ChatGPT对话时作为文本输入。  
解决方案：[百度SDK](https://login.bce.baidu.com/)

## ChatGPT
[OpenAI接口文档](https://platform.openai.com/docs/api-reference)  
[LangChain文档](https://python.langchain.com/)
### 工具定制
- 时间 系统时间调用 $\surd$
- LED灯 当Agent在思维链中调用工具时闪烁，提示用户Agent正在使用工具请等候 (待完成)
（此处Agent的定义请查阅LangChain文档）
- 雨水传感器、温度湿度传感器GPIO $\surd$ (与ChatGPT的接口已完成，引脚参数未设置)
- 天气 OpenWeatherMap API $\surd$
- 搜索引擎 Google API  $\surd$
- 计算 Wolramapla API  $\surd$
## 语音合成  
语音合成将文本信号转化为声音信号  
解决方案：[百度SDK](https://login.bce.baidu.com/)



# 调用顺序  
唤醒词进程一直等待监听
监听到唤醒词后调用语音识别模块
将语音识别模块的输出内容传给chat模块
将chat模块的输出内容传给语音合成模块