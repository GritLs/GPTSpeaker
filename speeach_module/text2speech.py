"""
语音合成模块，文本转语音，可选择百度、pyttsx3、edge_tts三种方案
三种方案都已实现，根据实际情况任选其一
播放声音的库是playsound和pygame，playsound不稳定时可用pygame（）
补充：修改playsound源码可以解决不稳定的问题
"""

from playsound import playsound
import pygame  # 导入pygame，playsound报错或运行不稳定时直接使用
import pyttsx3
import asyncio
from aip import AipSpeech
from edge_tts import Communicate

import os


class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        print("-------------------------------")
        print(text)
        print("###############################")
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per': 4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        playsound('audio.mp3')
        # self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式

    def play_audio_with_pygame(self, audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()


class Pyttsx3TTS:
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text=""):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


class EdgeTTS:
    def __init__(self, voice: str = "zh-CN-XiaoyiNeural", rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def text_to_speech_and_play(self, text):
        # voices = await VoicesManager.create()
        # voice = voices.find(Gender="Female", Language="zh")
        # communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
        communicate = Communicate(text, self.voice)
        await communicate.save('audio.mp3')
        playsound('audio.mp3')


if __name__ == '__main__':

    # 使用百度语音

    APP_ID = "32714532"
    API_KEY = "GgWZBkVHMtZb1dmpH3POKGB7"
    SECRET_KEY = "T2ewdGvihXBKEykoNuhpGhdufz3EOIqQ"
    baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    baidutts.text_to_speech_and_play("春天来了，每天的天气都很好！")

    # 使用pyttsx3

    # pyttsx3tts = Pyttsx3TTS()
    # pyttsx3tts.text_to_speech_and_play('春天来了，每天的天气都很好！')

    # 使用edge_tts

    # edgetts = EdgeTTS()
    # asyncio.run(edgetts.text_to_speech_and_play(
    #     "春天来了，每天的天气都很好！"))
