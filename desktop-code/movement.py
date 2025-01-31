import time
from gpiozero import AngularServo,LED,PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
import socket


raspberry_pi_ip = '192.168.1.15' 

#Host's IP Address (In Our Case The Pi's Address)
factory = PiGPIOFactory(host=raspberry_pi_ip)

#Servos    
hori_servo = AngularServo(15,min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=factory)
vert_servo = AngularServo(3,min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=factory)

#Declaring The Motors
motor1_forward=LED(21,pin_factory=factory)
motor1_backward=LED(20,pin_factory=factory)
motor2_forward=LED(19,pin_factory=factory)
motor2_backward=LED(26,pin_factory=factory)

#Indication LED
led = PWMLED(18,pin_factory=factory)


def led_indication(i):
        led.pulse()
        if i==0:
                led.value=0


def moveForward(i):
            motor1_forward.on()
            motor2_forward.on()
            time.sleep(i)
            motor1_forward.off()
            motor2_forward.off()
            
def moveBackward():
            motor1_backward.on()
            motor2_backward.on()
            time.sleep(0.6)
            motor1_backward.off()
            motor2_backward.off()
            
def turnLeft():
            motor1_forward.on()
            motor2_backward.on()
            time.sleep(0.3)
            motor1_forward.off()
            motor2_backward.off()
            
def turnRight():
            motor1_backward.on()
            motor2_forward.on()
            time.sleep(0.3)
            motor1_backward.off()
            motor2_forward.off()
            
def wakeUp():
    hori_servo.angle = 0
    vert_servo.angle = 0


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((raspberry_pi_ip, 9999))
    new_value = 'wake'  # String to update the variable
    client.send(new_value.encode())  # Send the value
    client.close()

    time.sleep(0.8)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((raspberry_pi_ip, 9999))
    new_value = 'idle'  # String to update the variable
    client.send(new_value.encode())  # Send the value
    client.close()    
    
def sleep():
    hori_servo.angle = 0
    vert_servo.angle = -45


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((raspberry_pi_ip, 9999))
    new_value = 'sleep'  # String to update the variable
    client.send(new_value.encode())  # Send the value
    client.close()


def motorOn():
        motor1_forward.on()
        motor2_forward.on()

def motorOff():
    motor1_forward.off()
    motor2_forward.off()

def xServo(i):
    hori_servo.angle = i

def yServo(i):
    if 0 <= i:
        vert_servo.angle = i