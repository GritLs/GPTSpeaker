from .MySnowboy import snowboydecoder
import sys
import signal

class VoiceWakeUp:
    def __init__(self, model, sensitivity=0.5, audio_gain=1):
        self.detector = snowboydecoder.HotwordDetector(model, sensitivity=sensitivity, audio_gain=audio_gain)
        self.interrupted = False
        self.wakeup_detected = False

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def on_detected(self):
        print("唤醒词已检测到！")
        self.wakeup_detected = True
        self.interrupted = True

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        print("等待唤醒词...")
        self.detector.start(detected_callback=lambda: self.on_detected(),
                            interrupt_check=self.interrupt_callback, sleep_time=0.03)
        return self.wakeup_detected

    def terminate(self):
        self.detector.terminate()
