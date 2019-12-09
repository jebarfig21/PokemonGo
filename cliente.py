#Programa que solicita conexión del lado del cliente
import socket

if __name__ == "__main__":
        print("Dirección ip servidor :")
        host = input()
        puerto = 9999

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, puerto))
                s.sendall(b"Conexion establecida")
                data = s.recv(1024) #maximo de 1024 bits de información de regreso

        print('Mensaje recibido', repr(data))
   
