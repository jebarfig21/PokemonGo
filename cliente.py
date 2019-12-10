#Programa que solicita conexión del lado del cliente
import socket

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



def conectarServidor(socket):
    print("Entrando conectarServidor")
#cominzo de la conexion con el codigo 10 representado en 1 byte
    codigo = bytes([10])
#Aqui el codigo que mandamos esta conformado por el codigo de inicio 10
    socket.send(codigo)
    print("saliendo conectarServidor")
    return None


def obtenerEntrenador(socket):
    print("entrando obtenerEntrenador")
    respuesta = socket.recv(2)
    print(respuesta[0])
    if respuesta[0] != SOLICITAR_ENTRENADOR: #codigo 11
            print("El codigo enviado no es el correcto")
            return None
    try:
        print("Introduce el id de tu entrenador:")
        IDentrenador = int(input())
    except ValueError:
        print('Numero de ID no reconocido')
        raise Exception
#Aqui el codigo que mandamos esta conformado por
#el id del entrenador en forma de 1 byte
    codigo =bytes([IDentrenador])
    #codigo = (IDentrenador).to_bytes(1, byteorder="little")
    print (codigo)
    socket.send(codigo)
    print("saliendo obtenerEntrenador")
    return entrenadores[IDentrenador]["entrenador"]
    #return None

def get_pokemon(pokemon_id):
    """
        Get a pokemon by its id
    """
    return pokemons.get(pokemon_id, {})

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("¿Cual es la direccion IP del servidor?:")
    host = input()
    puerto = 9999
    try:
        s.connect((host, puerto))
    except:
        print("Servidor no disponible")
        exit(404)

    print("Bienvenido entrenador al fascinante mundo de pokemon =)")

    try:
        conectarServidor(s)
        entrenador= obtenerEntrenador(s)
        print ("Bienvenido "+ entrenador)
        
    except:
        print("A ocurrido un error en la conexion y se cerrara.")
        s.send((ERROR_CONEXION).to_bytes(1, byteorder="little"))
    finally:
        s.close()
