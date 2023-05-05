from speeach_module.wakeup import VoiceWakeUp
from speeach_module.speech2text import BaiduASR
from speeach_module.text2speech import BaiduTTS
from gpt_module.chat import LangChainAgent
import os
import threading
import time
from iodevices.LED import LED
os.environ["SERPER_API_KEY"] = "" # 你的serper key
keyword_path = './speechmodules/Hey-Murphy_en_mac_v2_1_0.ppn'  # 你的唤醒词检测离线文件地址
wake_model = '/home/pi/Desktop/GPTSpeaker/speeach_module/MySnowboy/resources/models/HeyMurphy.pmdl' # 中文模型地址
Baidu_APP_ID = '32714532'  # 你的百度APP_ID
Baidu_API_KEY = 'GgWZBkVHMtZb1dmpH3POKGB7'  # 你的百度API_KEY
Baidu_SECRET_KEY = 'T2ewdGvihXBKEykoNuhpGhdufz3EOIqQ'  # 你的百度

# led = LED(11)
# def led_blink(stop_event):
#     while not stop_event.is_set():
#         # 灯闪烁的代码
#         led.on()
#         time.sleep(0.5)
#         led.off()
#         time.sleep(0.5)

# def led_off():
#     # 灯灭的代码
#     led.off()



def run(voiceWakeUp, asr, tts):
      # 需要始终保持对唤醒词的监听
    keyword_idx = voiceWakeUp.start()
    if keyword_idx:

        # led_blink_thread = None
        # stop_event = threading.Event()

        
        voiceWakeUp.terminate()  # 需要对取消对麦克风的占用!
        openai_chat_module = LangChainAgent()
        # print("嗯,我在,请讲！")
        tts.text_to_speech_and_play("嗯,我在,请讲！")
        while True:  # 进入一次对话session
            q = asr.speech_to_text()
            print(f'recognize_from_microphone, text={q}')
            #从这里开始灯闪
            # if led_blink_thread is None or not led_blink_thread.is_alive():
            #     stop_event.clear()
            #     led_blink_thread = threading.Thread(target=led_blink, args=(stop_event,), daemon=True)
            #     led_blink_thread.start()
            res = openai_chat_module.response(q)
            # stop_event.set()
            # led_blink_thread.join()  # 等待led_blink线程完成
            # led_off()
            #在这里灯灭
            print(res)
            tts.text_to_speech_and_play('嗯' + res)


def Orator():
    while True:
        sensitivity = 0.9
        audio_gain = 1
        voiceWakeUp = VoiceWakeUp(wake_model, sensitivity=sensitivity, audio_gain=audio_gain)
        asr = BaiduASR(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
        tts = BaiduTTS(Baidu_APP_ID, Baidu_API_KEY, Baidu_SECRET_KEY)
        # LED灯
        try:
            run(voiceWakeUp, asr, tts)
        except KeyboardInterrupt:
            print("中断检测")
            exit(0)
        finally:
            print('本轮对话结束')
            tts.text_to_speech_and_play('嗯' + '主人，我退下啦！')
            print("中断检测")
            voiceWakeUp.terminate() 

if __name__ == '__main__':
    Orator()