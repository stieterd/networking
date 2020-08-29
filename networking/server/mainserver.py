import socket
import time
import classes

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", classes.serverPort))

message = bytes("Hello", "utf-8")

connectedPorts = {}

while True:
	
	try:

		packet, addr = server.recvfrom(1024)

		packet = packet.decode('utf-8')
		data = packet.split("&")

		

		if data[0] == "connecting":

			if data[1] in connectedPorts:

				channelPorts = connectedPorts[data[1]]
				channelPorts.append(addr[1])
				connectedPorts[data[1]] = channelPorts

			elif data[1] not in connectedPorts:

				connectedPorts[data[1]] = [addr[1]]

			for client in connectedPorts[data[1]]:


				clientData = bytes(f"User {addr[1]} just connected to the channel", "utf-8") 
				server.sendto(clientData, ('<broadcast>', client))

			print(f"Port: {addr[1]}, just connected to channel: {data[1]}")

		elif data[0] == "disconnected":

			try:

				channelPorts = connectedPorts[data[1]]

				if len(channelPorts) <= 1:

					del connectedPorts[data[1]]

				elif len(channelPorts) > 1:

					channelPorts.remove(addr[1])
					connectedPorts[data[1]] = channelPorts

				for client in connectedPorts[data[1]]:

					clientData = bytes(f"User {addr[1]} just disconnected from the channel", "utf-8") 
					server.sendto(clientData, ('<broadcast>', client))

				

			except KeyError:

				pass

			print(connectedPorts)
			print(f"Port: {addr[1]}, just disconnected")


		else:

			try:

				for client in connectedPorts[data[1]]:

					if client != addr[1]:

						clientData = bytes(f"{addr[1]}: {data[0]}", "utf-8") 

					else:

						clientData = bytes(f"you({addr[1]}): {data[0]}", "utf-8") 
					
					server.sendto(clientData, ('<broadcast>', client))

			except KeyError:

				if data[1] in connectedPorts:

					channelPorts = connectedPorts[data[1]]
					channelPorts.append(addr[1])
					connectedPorts[data[1]] = channelPorts

				elif data[1] not in connectedPorts:

					connectedPorts[data[1]] = [addr[1]]

				for client in connectedPorts[data[1]]:

					if client != addr[1]:

						clientData = bytes(f"{addr[1]}: {data[0]}", "utf-8") 

					else:

						clientData = bytes(f"you({addr[1]}): {data[0]}", "utf-8") 
					
					server.sendto(clientData, ('<broadcast>', client))

	except socket.timeout:

		pass

	
	
	time.sleep(1)
	

