import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)  # 设置GPIO引脚编号模式为BOARD
        GPIO.setup(self.pin, GPIO.OUT)  # 将引脚设置为输出模式
        self.pwm = GPIO.PWM(self.pin, 1000)  # 创建PWM实例，设置频率为1000Hz
        self.pwm.start(0)  # 启动PWM，初始占空比为0
        self.current_brightness = 0  # 记录当前亮度级别

    def on(self):
        duty_cycle = (255 / 255) * 100  # 计算占空比
        self.pwm.ChangeDutyCycle(duty_cycle)  # 设置PWM的占空比
        self.current_brightness = 255  # 记录当前亮度级别

    def off(self):
        duty_cycle = (0 / 255) * 100  # 计算占空比
        self.pwm.ChangeDutyCycle(duty_cycle)  # 设置PWM的占空比
        self.current_brightness = 0  # 记录当前亮度级别

    def toggle(self):
        if GPIO.input(self.pin):
            self.off()  # 如果LED已经点亮，就关闭它
        else:
            self.on()  # 如果LED已经关闭，就点亮它

    # 这段代码是LEDController类的一个方法，用于设置LED的亮度级别。具体来说，它接受一个范围在0到255之间的整数值作为参数
    # `brightness`，用于设置LED的亮度级别。首先，它将 `brightness`
    # 除以255，得到一个0到1之间的小数值，然后再将其乘以100，得到一个0到100之间的占空比值。接下来，它使用`ChangeDutyCycle()`
    # 方法设置PWM的占空比，从而控制LED的亮度。最后，它将当前的亮度级别记录到
    # `self.current_brightness` 属性中，以便其他方法可以使用它。
    def set_brightness(self, brightness):
        duty_cycle = (brightness / 255) * 100  # 计算占空比
        self.pwm.ChangeDutyCycle(duty_cycle)  # 设置PWM的占空比
        self.current_brightness = brightness  # 记录当前亮度级别

    def increase_brightness(self, delta=10):
        new_brightness = min(self.current_brightness + delta, 255)  # 计算新的亮度级别
        self.set_brightness(new_brightness)  # 设置LED的亮度为新的亮度级别

    def decrease_brightness(self, delta=10):
        new_brightness = max(self.current_brightness - delta, 0)  # 计算新的亮度级别
        self.set_brightness(new_brightness)  # 设置LED的亮度为新的亮度级别

    def cleanup(self):
        GPIO.cleanup()  # 清理GPIO引脚的设置，释放资源


if __name__ == '__main__':
    try:
        led = LED(11)
        while True:
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
    finally:
        led.cleanup()