from tkinter import *
from threading import Thread, RLock
import queue



class Chat():
	def __init__(self, q, p, mutex):
		self.queue_v_s = q
		self.queue_f_s = p
		self.name = ""
		self.mutex = mutex

	def start_chat(self):
		self.windows_chat = Toplevel()
		self.windows_chat.title("Chat")
		self.windows_chat.geometry("300x300")
		self.windows_chat.resizable(False, False)
		self.windows2 = PhotoImage(file="./ressources/chat.png")
		self.windows3 = Label(self.windows_chat, image=self.windows2)
		self.windows3.pack()

		self.entry_msg_var = StringVar()
		self.entry_msg = Entry(self.windows_chat, textvariable=self.entry_msg_var, width=30)
		self.entry_msg.place(x=5,y=257)

		self.label_chat = Label(self.windows_chat, relief=FLAT, justify=LEFT, bg="white", width=20, height=12, text="")
		self.label_chat.place(x=5,y=47)


		self.send_button_img = PhotoImage(file="./ressources/chat_button.png")
		self.send_button = Button(self.windows_chat, text="", bg="white", relief=FLAT, image=self.send_button_img, command=self.send_msg)
		self.send_button.place(x=252, y=255)
		self.windows_chat.mainloop()

	def send_msg(self):
		print("Je passe par là")
		a = self.entry_msg_var.get().rstrip('\n')
		if (len(a) <= 0):
			return
		msg = self.name + ' : ' + a + '\n'
		with self.mutex:
			self.queue_v_s.put(msg)
			print("Je passe ici aussi")


	def update(self):
		try:
			try:
				with self.mutex:
					msg = self.queue_f_s.get()
			except queue.Empty:
				pass
			print(msg)
			self.label_chat["text"] = self.label_chat["text"] + msg
		except Exception as E:
			print(E)
			pass
