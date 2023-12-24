import Arm_Lib
import time
import requests
import pyfirmata
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

board = pyfirmata.Arduino('/dev/ttyUSB0')

time_interval = 3000 
server_check_interval = 10

def drink_serve(drink_type):
    Arm = Arm_Lib.Arm_Device()
    Arm.Arm_serial_servo_write6(0, 90, 90, 90, 90, 0, time_interval)
    time.sleep(time_interval/1000)
    Arm.Arm_serial_servo_write6(0, 10, 20, 160, 90, 0, time_interval)
    time.sleep(time_interval/500)
    Arm.Arm_serial_servo_write6(0, 10, 20, 160, 90, 70, time_interval)
    time.sleep(time_interval/700)  
    #컵 잡기
    Arm.Arm_serial_servo_write6(0, 25, 0, 165, 90, 70, time_interval)
    time.sleep(time_interval/1000)
    #조금 올리기 
    if drink_type == 1 :
        Arm.Arm_serial_servo_write6(70, 25, 0, 165, 90, 70, time_interval)
        time.sleep(time_interval/1000)
        board.digital[12].write(1)
        board.digital[13].write(0)
        time.sleep(time_interval/1000)
        board.digital[12].write(0)
        board.digital[13].write(0)
    elif drink_type == 2:
        Arm.Arm_serial_servo_write6(125, 25, 0, 165, 90, 70, time_interval)
        time.sleep(time_interval/1000)
        board.digital[12].write(1)
        board.digital[13].write(0)
        time.sleep(time_interval/1000)
        board.digital[12].write(0)
        board.digital[13].write(0)
    elif drink_type == 3:
        Arm.Arm_serial_servo_write6(180, 25, 0, 165, 90, 70, time_interval)
        time.sleep(time_interval/1000)
        board.digital[12].write(1)
        board.digital[13].write(0)
        time.sleep(time_interval/1000)
        board.digital[12].write(0)
        board.digital[13].write(0)
    
    time.sleep(time_interval/1000)
    Arm.Arm_serial_servo_write6(0, 25, 0, 165, 90, 70, time_interval)
    time.sleep(time_interval/1000)
    Arm.Arm_serial_servo_write6(0, 13, 20, 155, 90, 70, time_interval)
    time.sleep(time_interval/500)
    Arm.Arm_serial_servo_write6(0, 13, 20, 155, 90, 10, time_interval)
    time.sleep(time_interval/1000)
# 펌프 각도 
# 받는거: 0 
# 1번 펌프: 70
# 2번 펌프: 125
# 3번 펌프: 180
    

if __name__ == "__main__":
    while True:
        try:
            RST = None
            disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=1, gpio=1)
            disp.begin()
            disp.clear()
            disp.display()
            width = disp.width
            height = disp.height
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            padding = -2
            top = padding
            bottom = height-padding
            x = 0
            font = 'malgun.ttf'
            try:
                font = ImageFont.truetype(font, 9)
            except:
                font = ImageFont.load_default()
        except :
            time.sleep(1)
            continue
        break
    while True:
        orders = requests.get("https://mbp16.ez0.us/csclub/orders/").json()
        print("Orders: " + str(orders))
        for i in orders:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x, top), "Name: " + i["name"], font=font, fill=255)
            draw.text((x, top + 15), "Phone: " + i["phone"], font=font, fill=255)
            disp.image(image)
            disp.display()
            drink_serve(int(i["drink"]))
            requests.delete("https://mbp16.ez0.us/csclub/orders/", json={"name": i["name"]})
        print(str(server_check_interval) + " Seconds Starting")
        time.sleep(server_check_interval)
        print(str(server_check_interval) + " Seconds Over")
    
