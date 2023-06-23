from djitellopy import tello
import cv2

me = tello.Tello()
#cap = cv2.VideoCapture(0)
me.connect()
print('Connected!')
print("Tello battery: " + str(me.get_battery()))
me.streamon()


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    cv2.waitKey(1)

# from threading import Thread as th
# import socket
# from ctypes import windll as wdll
# import cv2

# # Title
# title = "TELLO Control Panel v.0.1.1 [DEVELOPMENT]"
# wdll.kernel32.SetConsoleTitleW(title)

# # Networking stuff
# class Net:
#     host = ''
#     port = 9000
#     locaddr = (host, port) 

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(locaddr)
#     tello_address = ('192.168.10.1', 8889)
#     def recv(self):
#         count = 0
#         while True: 
#             try:
#                 data, server = self.sock.recvfrom(1518)
#                 print("Response: " + data.decode(encoding="utf-8"))
#             except Exception:
#                 print('Exit . . .')
#                 break
#     recvThread = th(target=recv, daemon=True)
#     recvThread.start()
#     def send(self, msg):
#         msgEncoded = msg.encode("utf-8")
#         self.sock.sendto(msgEncoded, self.tello_address)

# class VideoOutput:
#     try:
#         Net.send(Net(), 'command')
#         Net.send(Net(), 'streamon')
#     except Exception as e:
#         print(f"[EXCEPTION]: {e}")

#     while True:
#         img = me.get_frame_read().frame
#         img = cv2.resize(img, (360, 240))
#         cv2.imshow("results", img)
#         cv2.waitKey(1)

