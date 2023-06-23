import tkinter as tk
import time


currentTime = time.strftime("%H:%M", time.localtime())
isSendMessage = False
class ChatBox:
    def __init__(self, master):
        title = "RYZE TELLO Control Panel v.0.1.0 [DEVELOPMENT]"
        self.master = master
        master.title(title)

        self.chat_window = tk.Text(master, bd=1, bg="white", width=50, height=8, wrap='none')
        self.chat_window.place(x=6, y=6, height=270, width=370)
        
        self.help_window = tk.Text(master, bd=1, bg="white", width=50, height=20, wrap='none')
        self.help_window.place(x=382, y=6, height=270, width=370)

        self.message_window = tk.Entry(master, bg="white", width=30)
        self.message_window.place(x=6, y=280, height=88, width=260)

        self.send_button = tk.Button(master, text="Отправить", command=self.send_message()) # type: ignore

        # self.send_button.place(x=270, y=280, height=65, width=105) - 1 вариант
        # self.send_button.place(x=270, y=280, height=88, width=90) - 2 вариант
        self.send_button.place(x=270, y=292, height=65, width=90)

        self.message_window.bind('<Return>', lambda event: self.send_message())

        scrollbarChat = tk.Scrollbar(self.chat_window)
        scrollbarChat.pack(side='right', fill='y')
        scrollbarHelp = tk.Scrollbar(self.help_window)
        scrollbarHelp.pack(side='right', fill='y')

        self.chat_window.config(yscrollcommand=scrollbarChat.set)
        scrollbarChat.config(command=self.chat_window.yview)
        self.help_window.config(yscrollcommand=scrollbarHelp.set)
        scrollbarHelp.config(command=self.help_window.yview)

        self.chat_window.config(state="disabled")
        self.help_window.config(state="disabled")

    def insertInChat(self, msg=""):
        self.chat_window.configure(state="normal")
        self.chat_window.insert(tk.END, f"[{currentTime}]> {msg}\n")
        self.chat_window.yview(tk.END)
        self.chat_window.configure(state="disabled")   
    def insertInHelp(self, msg):
        self.help_window.configure(state="normal")
        self.help_window.insert(tk.END, f"{msg}\n") # type: ignore
        self.help_window.configure(state="disabled")
    
    message = "started"

    def send_message(self):
        global isSendMessage
        global message
        message = "hui"
        return message
        # isSendMessage = True
        # message = self.message_window.get()

        # if message and not message.isspace():
        #     print(f"[{currentTime}]> {message}")
        #     self.insertInChat(message)
        #     self.message_window.delete(0, tk.END)

        # isSendMessage = False

        # return message,

root = tk.Tk()
chat_box = ChatBox(root)
root.geometry("758x375")
root.resizable(False, False)