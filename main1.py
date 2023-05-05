# from speeach_module import wakeup,speech2text,text2speech
from speeach_module.wakeup import VoiceWakeUp
from speeach_module.speech2text import BaiduASR
from speeach_module.text2speech import BaiduTTS
from gpt_module.chat import LangChainAgent



def main():
    """设置唤醒词模块的参数"""
    wake_model = "/home/pi/Desktop/GPTSpeaker/speeach_module/MySnowboy/resources/models/HeyMurphy.pmdl"
    sensitivity = 0.9
    wakeup_detector = VoiceWakeUp(model=wake_model,sensitivity=sensitivity)
    detected = wakeup_detector.start()
    if detected:
        wakeup_detector.terminate()
        
