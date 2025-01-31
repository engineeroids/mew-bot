import sys
import time
from PIL import Image
import st7735

import socket

# Create TFT LCD display class.
disp = st7735.ST7735(
    port=0,
    cs=st7735.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT. BG_SPI_CS_FRONT (eg: CE1) for Enviro Plus
    dc="GPIO24",                 # "GPIO9" / "PIN21". "PIN21" for a Pi 5 with Enviro Plus
    backlight="GPIO22",
    rst="GPIO25",# "PIN18" for back BG slot, "PIN19" for front BG slot. "PIN32" for a Pi 5 with Enviro Plus
    rotation=90,
    invert=False,
    spi_speed_hz=40000000
)

# Initialize display.
disp.begin()

width = disp.width
height = disp.height
frame = 0

variable = 'idle'

def handle_client(client_socket):
    global variable
    try:
        data = client_socket.recv(1024).decode()
        if data:
            variable = data
            print(f"Variable updated to: {variable}")
            client_socket.send(b"Value updated successfully")
    except BlockingIOError:
        pass  # No data received yet
    finally:
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 9999))
server.listen(5)
server.setblocking(False)

a = 0

while True:
    if 'idle' in variable and a!=1:
        image = Image.open('idle.gif')
        frame = 0
        a = 1
        
    elif 'happy' in variable and a!=2:
        image = Image.open('happy.gif')
        frame = 0
        a = 2
    elif 'angry' in variable and a!=3:
        image = Image.open('angry.gif')
        frame = 0
        a = 3
    elif 'confused' in variable and a!=4:
        image = Image.open('confused.gif')
        frame = 0
        a = 4
        
    elif 'love' in variable and a!=5:
        image = Image.open('love.gif')
        frame = 0
        a = 5
        
    elif 'sleep' in variable and a!=6:
        image = Image.open('sleep.gif')
        frame = 0
        a = 6
        
    elif 'wake' in variable and a!=7:
        image = Image.open('wake.gif')
        frame = 0
        a = 7

    try:
        image.seek(frame)
        #Adjustments As Per My Display
        frame_image = image.resize((width, height))
        frame_image = frame_image.transpose(Image.FLIP_TOP_BOTTOM)
        frame_image = frame_image.transpose(Image.FLIP_LEFT_RIGHT)
            
        disp.display(frame_image)
        frame += 1
        time.sleep(0.01)
        
        client, addr = server.accept()
        print(f"Connected by {addr}")
        handle_client(client)

    except EOFError:
        frame = 0
        
    except BlockingIOError:
        pass

