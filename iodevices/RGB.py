import RPi.GPIO as GPIO
import time

class RGBLED:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.setup_GPIO()  # 初始化GPIO设置

    def setup_GPIO(self):
        GPIO.setmode(GPIO.BCM)  # 设置GPIO模式为BCM模式
        GPIO.setup(self.red_pin, GPIO.OUT)  # 设置红色LED灯引脚为输出模式
        GPIO.setup(self.green_pin, GPIO.OUT)  # 设置绿色LED灯引脚为输出模式
        GPIO.setup(self.blue_pin, GPIO.OUT)  # 设置蓝色LED灯引脚为输出模式
        self.red_pwm = GPIO.PWM(self.red_pin, 500)  # 创建红色LED灯的PWM对象
        self.green_pwm = GPIO.PWM(self.green_pin, 500)  # 创建绿色LED灯的PWM对象
        self.blue_pwm = GPIO.PWM(self.blue_pin, 500)  # 创建蓝色LED灯的PWM对象
        self.red_pwm.start(0)  # 启动红色LED灯的PWM信号输出
        self.green_pwm.start(0)  # 启动绿色LED灯的PWM信号输出
        self.blue_pwm.start(0)  # 启动蓝色LED灯的PWM信号输出

    def set_color(self, red, green, blue):
        self.red_pwm.ChangeDutyCycle(red)  # 设置红色LED灯的亮度
        self.green_pwm.ChangeDutyCycle(green)  # 设置绿色LED灯的亮度
        self.blue_pwm.ChangeDutyCycle(blue)  # 设置蓝色LED灯的亮度

    def set_color_hex(self, hex_code):
        if len(hex_code) == 6:
            red = int(hex_code[0:2], 16) * 100 / 255  # 将十六进制的红色通道值转换为亮度值
            green = int(hex_code[2:4], 16) * 100 / 255  # 将十六进制的绿色通道值转换为亮度值
            blue = int(hex_code[4:6], 16) * 100 / 255  # 将十六进制的蓝色通道值转换为亮度值
            self.set_color(red, green, blue)  # 设置LED灯的颜色

    def cleanup(self):
        self.red_pwm.stop()  # 停止红色LED灯的PWM信号输出
        self.green_pwm.stop()  # 停止绿色LED灯的PWM信号输出
        self.blue_pwm.stop()  # 停止蓝色LED灯的PWM信号输出
        GPIO.cleanup()  # 清理GPIO设置并释放资源


if __name__ == '__main__':
    # 定义三个LED灯的引脚编号
    red_pin = 18
    green_pin = 23
    blue_pin = 24

    # 创建RGBLED对象
    led = RGBLED(red_pin, green_pin, blue_pin)

    # 循环改变LED灯的颜色
    colors = ["FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF"]
    for color in colors:
        print("Setting color: " + color)
        led.set_color_hex(color)   # 设置LED灯的颜色
        time.sleep(1)   # 延时1秒

    # 清理GPIO设置并释放资源
    led.cleanup()