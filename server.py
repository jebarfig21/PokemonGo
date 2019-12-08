import socket
import threading

# codigos que usaremos
SOLICITAR_CAPTURA = 10
PREGUNTAR_CAPTURA = 20
CAPTURAR_DE_NUEVO = 21
ENVIAR_POKEMON = 22
INTENTOS_AGOTADOS = 23
SI = 30
NO = 31
TERMINAR_SESION = 32

SOLICITAR_ENTRENADOR = 11
ERROR_CONEXION = 40
ERROR_CODIGO = 41

#Pokemones disponibles
pokemones = {
    1: ("charizard", "img/charizard.png"),
    2: ("dragonite", "img/dragonite.png"),
    3: ("eve", "img/eve.png"),
    4: ("oddish", "img/oddish.png"),
    5: ("peliper", "img/peliper.png"),
    6: ("pikachu", "img/pikachu.png"),
    7: ("togepi", "img/togepi.png")
}

#Entrenadores disponibles
entrenadores = {
    1: {'id': 1,
    	'entrenador': "Manuel",
        'atrapados': []},
    2: {'id': 2,
        'entrenador': "Diana",
        'Catched': []},
    3: {'id': 3,
        'entrenador': "Barajas",
        'atrapados': []}}

class servidor:
	#Iniciamos nuestro objeto
	def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))


    def pedirEntrenador(client, address):
    	#Solicitamos el id del entrenador
        client.send((SOLICITAR_ENTRENADOR).to_bytes(1, byteorder="little"))
    	codigo = client.recv(2)
    	id_entrenador = codigo[0]
    	#El id no esta en nuetra lista
    	if (id_entrenador not in entrenadores):
    		return {}

        return entrenadores.get(id_entrenador)
    	


    def escucha(self):
    	self.sock.listen(5)
        while True:
            #Siempre scuchamos nuevas peticiones
            client, address = self.socket.accept()
            # Ponemos nuetro Time Out
            client.settimeout(60)
            print("Se tiene una conexion con: " + address[0] + ":" + str(address[1]))
            # Creamos un nuevo thread por cada conexion
            threading.Thread(target = self.conexionCliente, args = (client, address)).start()

    def conexionCliente(self, client, address):
        try:
            self.print_socket_message(client, 'conectado')
            codigo = client.recv(2)
            cod = codigo[0]
            if code != CLIENT_CAPTURE: #Si el codigo enviado no fue 10, terminamos la conexion
            #mandamos un codigo de error
                client.send((ERROR_CODIGO).to_bytes(1, byteorder="little"))
                self.close_connection(client)
                return False

            entrenador = pedirEntrenador(client, address)
            if entrenador == {}:
            	self.close_connection(client)
                return False

            self.print_socket_message(client, str(entrenador))



        except socket.timeout:
            self.print_socket_message(client, "TIMEOUT")
          

            self.close_connection(client)
            return False


if __name__ == "__main__":
    print("Servidor iniciado")
    print("en espera")
    #escuchando en el puerto 9999
    servidor('', 9999)
    servidor.escucha()