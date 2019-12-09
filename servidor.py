#Programa que controla una conexión del lado del servidor para nuestro programa de pokemon Go.
import socket

PUERTO = 9999

class servidor:
    #Iniciamos nuestro objeto
    def __init__(self, host, port):
        self.host = host
        self.port = PUERTO
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def escucha(self):
        self.socket.listen()
        while True:
            conn, address = self.socket.accept()
            with conn:
                print('Conexión proveniente de :', address)

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                
                    conn.sendall(data)
            
if __name__ == "__main__":
    print("Iniciando ...")
    print("LISTENING ***")
    #escuchando en el puerto 9999
    servidor('', 9999).escucha()

