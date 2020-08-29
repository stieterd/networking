import curses 
import sys
import string
import clientnetwork


class Window:

	def __init__(self):

		self.running = True

		#__________INITIALIZING GUI WINDOW__________#
		screen = curses.initscr()
		self.height,self.width = screen.getmaxyx()
		self.win = curses.newwin(self.height,self.width,0,0)

		

		#__________INITIALIZING SOME VARS__________#
		self.connected = False
		self.typing = False
		self.message = []
		self.recvApp = clientnetwork.MyClient()

		self.recvdMsgs = []
		self.showrcvdMsgs = []
		self.showOffset = 0

	def main_operations(self):

		self.connect_server_window()

		self.server_window()

		print("You disconnected!")

	def connect_server_window(self):

		while self.connected == False:

			self.win.keypad(1)
			curses.curs_set(0)

			self.win.border(0)
			self.win.timeout(10)

			myKey = self.win.getch()

			self.win.clear()

			self.win.addstr(1, 2,"Do you want to connect to the server or quit? c/q: ")

			if myKey == ord("c"):

				channelCode = []

				while True:


					self.win.keypad(1)
					curses.curs_set(0)

					self.win.border(0)
					self.win.timeout(100)

					inputKey = self.win.getch()

					self.win.clear()

					self.win.addstr(1, 2,"Give the channel code you want to use: ")

					

					if 0 < inputKey < 250:

						if (inputKey) == 8: #BACKSPACE

							channelCode = channelCode[:-1]

						elif inputKey == 10: #ENTER

							if channelCode != []:

								self.myChannel = "".join(channelCode)
								break

						elif chr(inputKey) in string.digits:

							channelCode.append(chr(inputKey))

					for idx in range(len(channelCode)):

						self.win.addch(1, 41 + idx, (channelCode[idx]))





				self.recvApp.connecting(str(self.myChannel))
				self.connected = True

			elif myKey == ord("q"):

				break

	def server_window(self):

		self.maxIdx = (self.height-5)//2 - 2

		while self.connected:

	

			self.win.keypad(1)
			curses.curs_set(0)

			self.win.border(0)
			self.win.timeout(2)

			myKey = self.win.getch()

			self.win.clear()

			if myKey == curses.KEY_END:

				self.recvApp.send_message("disconnected", self.myChannel)
						
				self.connected = False

			if myKey == ord(" "):

				self.typing = True

			if myKey == curses.KEY_UP and (len(self.recvdMsgs)-1 - (self.maxIdx + 1))+ self.showOffset > 0:

				self.showOffset -= 1

			elif myKey == curses.KEY_DOWN and self.showOffset < 0:

				self.showOffset += 1

			elif myKey == 27:

				self.message = []
				self.typing = False
			
			self.win.addstr(1, 2,"Start of your discussion:")
			self.win.addstr(1, self.width - 50, f"You're in channel: {self.myChannel}")

			for idx in range(self.width):

				self.win.addch(2, idx, "-")
				self.win.addch(self.height-3, idx, "-")

			if self.typing == False:
				self.win.addstr(self.height-2, 2, "Press spacebar to start typing:")

			else:
				self.win.addstr(self.height-2, 2, "Press esc to stop typing:")


			clientReturn = self.recvApp.recv_message()

			if clientReturn != None:

				self.recvdMsgs.append(clientReturn)



			if len(self.recvdMsgs)-1 - (self.maxIdx + 1 + self.showOffset) < 0:

				self.showrcvdMsgs = self.recvdMsgs[:]

			else:

				self.showrcvdMsgs = self.recvdMsgs[(len(self.recvdMsgs)-1 - (self.maxIdx + 1))+ self.showOffset:(len(self.recvdMsgs) + self.showOffset)] 



			for idx in range(len(self.showrcvdMsgs)):

				self.win.addstr(idx * 2 + 3, 2, self.showrcvdMsgs[idx])

			if self.typing == True:

				if 0 < myKey < 250:

					if (myKey) == 8: #BACKSPACE

						self.message = self.message[:-1]

					elif myKey == 10: #ENTER

						if len(self.message) == 0:

							pass

						else:

							self.recvApp.send_message("".join(self.message), self.myChannel)
							self.typing = False
							self.message = []

					elif chr(myKey) in string.ascii_letters + string.punctuation + string.digits or chr(myKey) == " ":

						if chr(myKey) == " " and len(self.message) == 0:

							pass

						else:
							self.message.append(chr(myKey))

				try:

					for idx in range(len(self.message)):

						self.win.addch(self.height-2, 28 + idx, (self.message[idx]))

				except:

						self.message = self.message[:-1]

						for idx in range(len(self.message)):

							self.win.addch(self.height-2, 28 + idx, (self.message[idx]))




wind = Window()
wind.main_operations()