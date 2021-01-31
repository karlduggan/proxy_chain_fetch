import socket
def check_port_is_open(ip, port):
	a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	location = (ip, port)
	result_of_check = a_socket.connect_ex(location)
	# if the port works then we get 0
	if result_of_check == 0:
		a_socket.close()
		return (ip, port)
	a_socket.close()
	return False
print(check_port_is_open('14.207.62.111', 8080))

