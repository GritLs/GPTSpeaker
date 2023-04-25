"""
语音唤醒模块，唤醒词为“Hey Murthy”
Hey-Murthy_en_windows_v2_2_0.ppn和Hey-Murthy_en_raspberry-pi_v2_2_0.ppn是唤醒词检测模型文件，
在树莓派系统中用后者可以离线唤醒（但是后续模块都需要联网）
"""

import pvporcupine
import pyaudio
import struct

PICOVOICE_API_KEY = "ECbJmXa2f6wwlhTXXjTEjI6aAhLl6vexW9iijvCJvugu9us1pHDv1w=="  # picovoice key
keyword_path = '/home/pi/Desktop/GPTSpeaker/speeach_module/Hey-Murthy_en_raspberry-pi_v2_2_0/Hey-Murthy_en_raspberry-pi_v2_2_0.ppn'  # 你的唤醒词检测离线文件地址


class PicoWakeWord:
    def __init__(self, PICOVOICE_API_KEY, keyword_path):
        self.PICOVOICE_API_KEY = PICOVOICE_API_KEY
        self.keyword_path = keyword_path
        self.porcupine = pvporcupine.create(
            access_key=self.PICOVOICE_API_KEY,
            keyword_paths=[self.keyword_path]
        )
        self.myaudio = pyaudio.PyAudio()
        self.stream = self.myaudio.open(
            # input_device_index=3,
            # rate=self.porcupine.sample_rate,
            rate=44100,
            # channels=1,
            channels=2,
            format=pyaudio.paInt16,
            input=True,
            # frames_per_buffer=self.porcupine.frame_length
            frames_per_buffer=1024
        )

    def detect_wake_word(self):
        audio_obj = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, audio_obj)
        keyword_idx = self.porcupine.process(audio_obj_unpacked)
        return keyword_idx


if __name__ == '__main__':
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    while True:
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            print("我听到了！")
