#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
# 
# Modified 14/06/2023 by Quezka (started 30/04/2023)
# Tello Control Panel v.0.1.2
#
# 1/1/2018; 30/04/2023; 14/06/2023

import threading 
import socket
import sys
import time
import platform  
import ctypes
import tkinter as tk
import djitellopy as tello
import cv2
import filePulling as save

title = "TELLO Control Panel v.0.1.2 [DEVELOPMENT]"
ctypes.windll.kernel32.SetConsoleTitleW(title)

# localMessage = gui.message
# oldLocalMessage = localMessage

# What's your machine?
host = ''
port = 9000
locaddr = (host, port) 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(locaddr)
tello_address = ('192.168.10.1', 8889)

# What're the variables?
commandList = "Available commands: \nhelp; \nend; \ncommand; \ntakeoff; \nland; \nemergency; \nup [distance 20-500cm]; \ndown [distance 20-500cm]; \nleft [distance 20-500cm]; \nright [distance 20-500cm]; \nforward [distance 20-500cm]; \nback [distance 20-500cm]; \ncw [rotates clockwise 1-3600 degrees]; \nccw [rotates counter-clockwise 1-3600 degrees]; \nflip [do a flip! l-left, r-right, f-forward, b-back]; \ngo [x y z] [speed (cm/s)]; \ncurve [x1 y1 z1] [x2 y2 z2] [speed cm/s]; \nspeed [10-100 cm/s]; \nrc [a b c d -100~100, a-left/right, b-forward/back, c-up/down, d-yaw]; \nwifi [ssid] [pass]; speed?; battery?; \ntime? - flight time; \nheight?; \ntemp?; \nattitude?; \nbaro?; \nacceleration?; \ntof?; \nwifi?; \nshowtime - programmed test sequence; \nread [filename] - pulls instructions from a .txt file separated by ';'; \nshowprogram - show imported program; \nrunprogram - runs pulled program."
commandListSimple = ['help', 
                     'end', 
                     'command', 
                     'takeoff', 
                     'land', 
                     'emergency', 
                     'up', 
                     'down', 
                     'left', 
                     'right', 
                     'forward', 
                     'back', 
                     'cw',
                     'ccw', 
                     'flip', 
                     'go', 
                     'curve', 
                     'speed', 
                     'rc', 
                     'wifi', 
                     'speed?', 
                     'battery?', 
                     'time?', 
                     'height?', 
                     'temp?', 
                     'attitude?', 
                     'baro?', 
                     'acceleration?', 
                     'tof?', 
                     'wifi?', 
                     'showtime',
                     'cum',
                     'video',
                     'read',
                     'showprogram',
                     'runprogram']
currentTime = time.strftime("%H:%M", time.localtime())
drone = tello.Tello()

# Define send
def send(msg):
    msgEncoded = msg.encode("utf-8")
    sock.sendto(msgEncoded, tello_address)

class ChatBox:
    def __init__(self, master):
        title = "RYZE TELLO Control Panel v.0.1.2 [DEVELOPMENT]"
        self.master = master
        master.title(title)
        self.program = []
        self.programName = ""

        self.chat_window = tk.Text(master, bd=1, bg="white", width=50, height=8, wrap='word')
        self.chat_window.place(x=6, y=6, height=270, width=419)
        
        self.help_window = tk.Text(master, bd=1, bg="white", width=50, height=20, wrap='word')
        self.help_window.place(x=429, y=6, height=270, width=370)

        self.message_window = tk.Entry(master, bg="white", width=30)
        self.message_window.place(x=6, y=280, height=88, width=260)

        self.send_button = tk.Button(master, text="Отправить", command=self.send_message)

        # self.send_button.place(x=270, y=280, height=65, width=105) - 1 вариант
        # self.send_button.place(x=270, y=280, height=88, width=90) - 2 вариант
        self.send_button.place(x=270, y=292, height=65, width=90)

        self.message_window.bind('<Return>', lambda event: self.send_message())

        # scrollbarChat = tk.Scrollbar(self.chat_window)
        # scrollbarChat.pack(side='right', fill='y')
        scrollbarHelp = tk.Scrollbar(self.help_window)
        scrollbarHelp.pack(side='right', fill='y')

        # self.chat_window.config(yscrollcommand=scrollbarChat.set)
        # scrollbarChat.config(command=self.chat_window.yview)
        self.help_window.config(yscrollcommand=scrollbarHelp.set)
        scrollbarHelp.config(command=self.help_window.yview)

        self.chat_window.config(state="disabled")
        self.help_window.config(state="disabled")
    def insertInChat(self, msg=""):
        self.chat_window.configure(state="normal")
        self.chat_window.insert(tk.END, f"[{currentTime}] {msg}\n")
        self.chat_window.yview(tk.END)
        self.chat_window.configure(state="disabled")   
    def insertInHelp(self, msg):
        self.help_window.configure(state="normal")
        self.help_window.insert(tk.END, f"{msg}\n") # type: ignore
        self.help_window.configure(state="disabled")

    def show(self):
        try:
            msgShow1 = "command"
            send(msgShow1)
            self.insertInChat("Connection established. Initiating showtime!")

            time.sleep(2)

            msgShow2 = "takeoff"
            send(msgShow2)
            self.insertInChat(msgShow2)

            time.sleep(2)
            
            msgShow3 = "up 20"
            send(msgShow3)
            self.insertInChat(msgShow3)

            time.sleep(2)

            msgShow4 = "cw 360"
            send(msgShow4)
            self.insertInChat(msgShow4)

            time.sleep(2)

            msgShow5 = "emergency"
            send(msgShow5)
            self.insertInChat(msgShow5)

            time.sleep(2)

            msgShow6 = "command"
            send(msgShow6)
            self.insertInChat("Connection closed. Showtime finished!")

        except KeyboardInterrupt: 
            self.insertInChat("[EXCEPTION] Interrupted by user.")
    # ChatGPT version:
    def send_message(self):
        msg = self.message_window.get()
        isFindSuccesful = False
        if msg and not msg.isspace():
            # Разбиваем введенную пользователем строку на отдельные слова
            words = msg.split()
            if len(words) > 0:
                command = words[0]
                # Проверяем, начинается ли первое слово команды с одного из элементов списка commandListSimple
                for c in commandListSimple:
                    if command.startswith(c):
                        print(f"Found! {command}")
                        print(f"[{currentTime}]> {msg}")
                        if command == 'help' or 'cum' or 'showtime' or 'video' or 'read' or 'showprogram' or 'runprogram':
                            isFindSuccesful = True
                            self.message_window.delete(0, tk.END)
                            self.insertInChat(msg)

                            if command == "help": 
                                self.insertInChat(commandList)
                            elif command == "cum": 
                                self.insertInChat('> cum')
                            elif command == 'showtime': 
                                self.show()
                            elif command == 'video':
                                VideoOutput.video(VideoOutput())
                            elif command == 'read':
                                msglist = msg.split(' ')
                                self.programName = msglist[1]

                                if len(msglist) < 2:
                                    self.insertInChat(f"Please specify the directory of the file you want to read!")
                                else:
                                    self.program = save.read_file(msglist[1]) 
                                    time.sleep(0.5)
                                    self.insertInChat(f"File read: {msglist[1]}!") 
                                    print(f"Program read: {self.program}") 
                            elif command == 'showprogram':
                                if self.program != None and self.program != " ":
                                    self.insertInChat(f"Your imported program: \n{'; '.join(self.program)}")
                                else:
                                    self.insertInChat(f"You haven't opened any files!")     
                            # self.insertInChat(msg)
                            elif command == 'runprogram':
                                if self.program != None and self.program != '':
                                    self.insertInChat(f"Running {self.programName}")
                                    for cmd in self.program:
                                        send(cmd)
                                        print(f"{cmd} sent!")
                                else:
                                    self.insertInChat("Program is not defined!")
                        else:
                            self.message_window.delete(0, tk.END)
                            self.insertInChat(msg)
                            send(msg)
                            isFindSuccesful = True
                            break
                        if not isFindSuccesful:
                            self.insertInChat(msg)
                            self.message_window.delete(0, tk.END)
                            self.insertInChat("Unknown command.")    

    # def send_message(self):
    #     msg = self.message_window.get()
    #     isFindSuccesful = False
    #     if msg and not msg.isspace():
    #         for command in commandListSimple:
    #             isFindSuccesful = False
    #             if msg in command:
    #                 print(f"Found!")
    #                 print(f"[{currentTime}]> {msg}")
    #             # if command.find(msg) != -1: 
    #                 print(f"index: {command.find(msg)}")
    #                 print(f"[{currentTime}]> {msg}")
    #                 if msg == "help": 
    #                     self.insertInChat(commandList)
    #                 elif msg == "cum": 
    #                     self.insertInChat('> cum')
    #                 elif msg == 'showtime': 
    #                     self.show()                   
    #                 self.insertInChat(msg)
    #                 self.message_window.delete(0, tk.END)
    #                 send(msg)
    #                 isFindSuccesful = True
    #             #     break
    #         if not isFindSuccesful:
    #             self.insertInChat(msg)
    #             self.message_window.delete(0, tk.END)
    #             self.insertInChat("Unknown command.")
class VideoOutput:
    def video(self):
        try:
            drone.streamon()
            img = drone.get_frame_read().frame
            img = cv2.resize(img, (1280, 720))
            cv2.imshow("TELLO Video Output", img)
            cv2.waitkey(1)
        except Exception as e:
            ChatBox.insertInChat(ChatBox(tk.Tk()), f"[EXCEPTION]: {e}")

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            chat_box.insertInChat(data.decode(encoding="utf-8"))
            print("Response: " + data.decode(encoding="utf-8"))
        except Exception:
            chat_box.insertInChat('Exit . . .')
            break

recvThread = threading.Thread(target=recv, daemon=True)
recvThread.start()

# Program start
root = tk.Tk()
root.geometry("805x375")
root.resizable(False, False)
root.iconbitmap("C:/Users/arsdo/Desktop/TelloControlPanel/icon.ico")
chat_box = ChatBox(root)
print(title)
chat_box.insertInHelp(title)
chat_box.insertInHelp(commandList)
root.mainloop()