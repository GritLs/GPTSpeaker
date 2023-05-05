"""
语音识别模块，语音转文本，用百度语音服务
挂梯子无法运行，解决方案为在改代码运行之前设置环境变量，os.environ['no_proxy'] = '*'（需要import os），可以让代码绕过代理
os.environ['no_proxy']默认是空，del os.environ['no_proxy']操作恢复其默认值。
"""


from aip import AipSpeech
import speech_recognition as sr
import os


class BaiduASR:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.r = sr.Recognizer()

    # 从麦克风收集音频并写入文件
    def _record(self, if_cmu: bool = False, rate=16000):
        with sr.Microphone(sample_rate=rate) as source:
            # 校准环境噪声水平的energy threshold
            # duration:用于指定计算环境噪声的持续时间（秒）。默认值为1秒。函数将等待指定时间来计算环境噪声水平，并相应地调整麦克风增益，以提高语音识别的准确性。如果噪声水平很高，则可以增加此值以获得更准确的噪声估计。
            self.r.adjust_for_ambient_noise(source, duration=1)
            print('您可以开始说话了')
            # timeout 用于指定等待语音输入的最长时间（秒），如果没有检测到语音输入，则函数将返回None。默认值为 None，表示等待无限长的时间。如果指定了超时时间，则函数将在等待指定时间后自动返回。
            # phrase_time_limit：用于指定允许单次语音输入的最长时间（秒），如果超过这个时间，函数将自动停止录制，并返回None.默认值为 None，表示允许单次语音输入的时间没有限制。
            audio = self.r.listen(source, timeout=15, phrase_time_limit=5)

        # file_name = "/home/pi/Desktop/GPTSpeaker/speeach_module/speech.wav"
        file_name = "./speech.wav"
        with open(file_name, "wb") as f:
            f.write(audio.get_wav_data())

        if if_cmu:
            return audio
        else:
            return self._get_file_content(file_name)

    # 从本地文件中加载音频 作为后续百度语音服务的输入
    def _get_file_content(self, file_name):
        with open(file_name, 'rb') as f:
            audio_data = f.read()
        return audio_data

    def speech_to_text(self, audio_path: str = "test.wav", if_microphone: bool = True):
        # 麦克风输入 采样频率必须为8的倍数 我们使用16000和上面保持一致
        if if_microphone:
            result = self.client.asr(self._record(), 'wav', 16000, {
                'dev_pid': 1537  # 识别中文普通话
            })
        # 从文件中读取
        else:
            result = self.client.asr(self._get_file_content(audio_path), 'wav', 16000, {
                'dev_pid': 1537  # 识别中文普通话
            })
        if result["err_msg"] != "success.":
            return "语音识别失败：" + result["err_msg"]
        else:
            return result['result'][0]


if __name__ == '__main__':
    APP_ID = "32714532"
    API_KEY = "GgWZBkVHMtZb1dmpH3POKGB7"
    SECRET_KEY = "T2ewdGvihXBKEykoNuhpGhdufz3EOIqQ"
    baiduasr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)
    result = baiduasr.speech_to_text()
    print(result)
