import socket
import keyboard
import sys
import random
import time
import classes



class MyClient:

	def __init__(self):

		self.serverPort = classes.serverPort
		#self.serverIp = "tcp://2.tcp.ngrok.io"
		self.serverIp = ""


		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.client.settimeout(0.01)
		self.client.bind(("", random.randint(1000, 9999)))

	def connecting(self, channelCode):

		self.client.sendto(bytes(f'connecting&{channelCode}', 'utf-8'), ('<broadcast>', self.serverPort))

	def send_message(self, message, channelCode):

		packet = bytes(f"{message}&{channelCode}", "utf-8")
		self.client.sendto(packet, ('<broadcast>', classes.serverPort))
	
	def recv_message(self):

		try:

			data, addr = self.client.recvfrom(1024)

			return data.decode('utf-8')

		except socket.timeout:

			return None
