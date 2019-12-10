import socket
import os

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
    1: {'id': 1, 'name': 'pikachu'},
    2: {'id': 2, 'name': 'peliper'},
    3: {'id': 3, 'name': 'oddish'},
    4: {'id': 4, 'name': 'eve'},
    5: {'id': 5, 'name': 'dragonite'},
    6: {'id': 6, 'name': 'charizard'},
    7: {'id': 7, 'name': 'togepi'}
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


#conexion servidor
def conectarServidor(socket):
#cominzo de la conexion con el codigo 10 representado en 1 byte
    codigo = bytes([10])
#Aqui el codigo que mandamos esta conformado por el codigo de inicio 10
    socket.send(codigo)
    return None

#Seleccionar entrenador
def obtenerEntrenador(socket):
    respuesta = socket.recv(2)
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
    socket.send(codigo)
    print("saliendo obtenerEntrenador")
    print("Bienvenido "+ entrenadores[IDentrenador]["entrenador"])

    return entrenadores.get(IDentrenador)

#Convertimos bytes a int
def bytes_converter(bytes):
    conversion = 0
    for b in bytes:
        conversion = conversion * 256 + int(b)
    return conversion

#Intentamos capturar al pokemon
def capture_pokemon(sock, trainer):
    respuesta = sock.recv(2)
    pokemon = pokemons.get(respuesta[1])
    print("Apareció " + pokemon.get('name', '') + " en tu camino, ¿Lo quieres atrapar? (y/n)")
    decision = input()
    atrapar_pokemon = 'y' ==  decision
    if not atrapar_pokemon:
        codigo = bytes([NO])
        print("¡Hasta la próxima!")
        sock.send(codigo)
        return None
    codigo = bytes([SI])
    sock.send(codigo)
    respuesta = sock.recv(3)
    while respuesta[0] == CAPTURAR_DE_NUEVO:
        #mensajes
        print(  pokemon.get('name', ''), "fue muy fuerte y no se dejo capturar")
        print("Te quedan", respuesta[2], "intento(s).\n")
        print("¿Quieres intentarlo una vez más y  capturar a " + pokemon.get('name', '') + "? (y/n) ")
        intento = input()
        atrapar_pokemon = 'y' == intento
        if not atrapar_pokemon:
            codigo = bytes([NO])
            sock.send(codigo)
            print("¡Hasta la próxima!")
            return None
        codigo = bytes([SI])
        sock.send(codigo)
        respuesta = sock.recv(3)
    if respuesta[0] == ENVIAR_POKEMON:
        print("¡Has atrapado a "+pokemon.get('name', ''), "!")
        print("¡Continua tu camino como entrenador pokemon!")


        #tam imagen
        tam = bytes_converter(respuesta[2:3] + sock.recv(3))
        tam = 200000
        img_bytes = sock.recv(tam)
        archivo = open("pokemones_capturados/" + pokemon['name'] + ".png", "wb")
        archivo.write(img_bytes)
        archivo.close()
        print("Tu pokemon se guardó en : pokemones_capturados/" + pokemon['name'] + ".png")
    elif respuesta[0] == INTENTOS_AGOTADOS:
        print("El pokemon escapó ")
        print("¡Hasta la próxima!")
    elif respuesta[0] == ERROR_CONEXION:
        print("Se cerró la conexión con el servidor")
    else:
        print("Algo salió mal  ")
    return None





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
        capture_pokemon(s, entrenador)
    except:
        print("Se cierra la conexión")
        s.send((ERROR_CONEXION).to_bytes(1, byteorder="little"))
    finally:
        s.close()
