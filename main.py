import Arm_Lib
import time
import requests
import pyfirmata

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
        orders = requests.get("https://mbp16.ez0.us/csclub/orders/").json()
        print("Orders: " + str(orders))
        for i in orders:
            drink_serve(int(i["drink"]))
            requests.delete("https://mbp16.ez0.us/csclub/orders/", json={"name": i["name"]})
        print(str(server_check_interval) + " Seconds Starting")
        time.sleep(server_check_interval)
        print(str(server_check_interval) + " Seconds Over")
    
