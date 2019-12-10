#Programa que controla una conexión del lado del servidor para nuestro programa de pokemon Go.
import socket
import threading
import os
from random import randint

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
pokemons = {
    1: {'id': 1, 'nombre': 'pikachu'},
    2: {'id': 2, 'nombre': 'peliper'},
    3: {'id': 3, 'nombre': 'oddish'},
    4: {'id': 4, 'nombre': 'eve'},
    5: {'id': 5, 'nombre': 'dragonite'},
    6: {'id': 6, 'nombre': 'charizard'},
    7: {'id': 7, 'nombre': 'togepi'}
}

#Entrenadores disponibles
entrenadores = {
    1: {'id': 1,
    	'entrenador': "Manuel",
        'atrapados': []},
    2: {'id': 2,
        'entrenador': "Diana",
        'atrapados': []},
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

    #Solicitamos el id del entrenador
    def pedirEntrenador(self,client, address):
        client.send((SOLICITAR_ENTRENADOR).to_bytes(1, byteorder="little"))
        codigo = client.recv(2)
        print ("pedir entrenador")
        id_entrenador = codigo[0]
        #El id no esta en nuetra lista
        if (id_entrenador > 3):
            return {}
        return entrenadores.get(id_entrenador)

    #Verificación codigo conexion
    def comprueba10(self,client, address):
        codigo = client.recv(2)
        cod = codigo[0]
        if cod != SOLICITAR_CAPTURA: #Si el codigo enviado no fue 10, terminamos la conexion
            #y mandamos un codigo de error
            return False
        return True


    #Servidor esta pendiente a las peticiones
    def escucha(self):
        self.socket.listen(5)
        while True:
            #Siempre escuchamos nuevas peticiones
            client, address = self.socket.accept()
            # Ponemos nuetro Time Out
            client.settimeout(60)
            print("Se tiene una conexion con: " + address[0] + ":" + str(address[1]))
            # Creamos un nuevo thread por cada conexion
            threading.Thread(target = self.conexionCliente, args = (client, address)).start()

    #metodo que maneja  la conexion con el cliente
    def conexionCliente(self, client, address):
        try:
            #comprobamos que se haya recibido el codigo 10 de inicio
            comprueba = self.comprueba10(client, address)
            if comprueba == False:
                codigo = bytes([ERROR_CODIGO])
                client.send(codigo)
                client.close()
                return False
            #pedimos el id del entrenador
            entrenador = self.pedirEntrenador(client, address)
            if entrenador == {}:
                print(client.getpeername()[0] + ' : ' + 'desconectado')
                client.close()
                return False
            
            print(str(entrenador))
            #mandamos al pokemon que se quiere capturar 
            pokemon = self.captura_pokemon(client, address)
            if pokemon != {}:
                #si se capturo al pokemon lo agregamos al pokedex del entrenador
                entrenador['atrapados'].append(pokemon)
                print(entrenador.get('entrenador', "") + " tiene a a los pokemones " + str(entrenador.get('atrapados', [])))
                print(client.getpeername()[0] + ' : ' + 'desconectado')
            client.close()
            #terminamos la conexion
            return True

        except socket.timeout:
            #si se acaba el timeout
            print(client.getpeername()[0] + ' : ' +'TIMEOUT')
            error = bytes([ERROR_CODIGO])
            client.send(error)
            client.close()
            return False

    #tamaño imagen a bytes
    def img_bytes(self, tam):
        array = []
        while tam >= 256:
            array.append(tam % 256)
            tam = tam // 256
        array.append(tam)
        array.reverse()
        b = b''
        for i in range(4-len(array)):
            b += b'\x00'
        b += bytes(array)
        return b

    #Mandar info imagen
    def mandar_pokemon(self, pokemon):
        img = pokemon["nombre"] + ".png"
        ubicacion = "img/"
        dir= ubicacion + img
        codigo = bytes([ENVIAR_POKEMON])
        codigo += bytes([pokemon['id']])
        tam = os.path.getsize(dir)
        f = open(dir, "rb")
        codigo += self.img_bytes(tam)
        codigo += f.read()
        f.close()
        return codigo

    #Atrapar al pokemon
    def captura_pokemon(self, client, address):
        pokemon_salvaje = pokemons[randint(1, len((pokemons.keys())))]
        codigo = bytes([PREGUNTAR_CAPTURA])
        codigo += bytes([pokemon_salvaje.get('id')])
        client.send(codigo)
        respuesta = client.recv(2)
        actual_num_attemps = randint(2, 10)
        while respuesta[0] == SI and actual_num_attemps > 0 :
            # numero de intentos aleatorios
            catch_pokemon = randint(0,100)
            if catch_pokemon < 35:
                codigo = self.mandar_pokemon(pokemon_salvaje)
                client.send(codigo)
                return pokemon_salvaje
            actual_num_attemps -= 1
            # numero de intentos usados
            if actual_num_attemps <= 0:
                break
            codigo = bytes([CAPTURAR_DE_NUEVO])
            codigo += bytes([pokemon_salvaje.get('id', -1)])
            codigo += bytes([actual_num_attemps])
            client.send(codigo)  #21
            respuesta = client.recv(2)
        if respuesta[0] == SI or actual_num_attemps <= 0:
            client.send(bytes([INTENTOS_AGOTADOS]))
            print(client.getpeername()[0] + ' : ' + 'desconectado')
            return {}
        elif respuesta[0] == NO:
            print("El entrenador no lo quiso capturar")
            return {}
        else:
            print("respuesta no válida")
            return {}


if __name__ == "__main__":
    print("Servidor iniciado")
    print("en espera")
    #escuchando en el puerto 9999
    servidor('', 9999).escucha()
