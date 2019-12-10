.. PokemonGo documentation master file, created by
   sphinx-quickstart on Mon Dec  9 13:56:56 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentación de Pokemon Go !
=====================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

UNIVERSIDAD NACIONAL AUTONOMA DE MEXICO

Este proyecto es correpondiente al proyecto 2 de la materia de Redes de Computadoras, curso impartido por el profesor Paulo Contreras Flores en el semestre 2020-1. Licenciatura en Ciencias de la Computación


Cliente
************************
    - conectarServidor : Función que manda la solicitud de conexión a un servidor.
    
    - obtenerEntrenador : Función que solicita la autenticación de un entrenador o usuario, en caso de no existir solicita de nuevo intentar autenticarse
    
    - bytes_converter : Función auxiliar que convierte elementos de tipo bytes a tipo entero
    
    - capture_pokemon : Función que ofrece un Pokemon a capturar, si se decide empezar a capturar se tienen hasta 10 intentos, el numero de intentos se escoge de manera aleatorio entre 2 y 10, al pasar estos 10 intentos(máximo) intentos el Pokemon escapa, el mejor escenario es capturar al pokemon, si esto pasa se guarda en pokemon capturados. 

Servidor
************************
\item pedirEntrenador : Se solicita el id del entrenador, como utilizamos un diccionario en python la autenticación la hicimos directo a buscar en el diccionario si se encuentra, si el número es mayor que el número máximo de elemento, simplemente rechazamos, por ahora el número de límite lo pusimos manualmente
    
    - comprueba10 : Método que comprueba que el código de solicitud de conexión haya sido 10\\
    
    - escucha : Método que abre nuestro socket del lado del servidor en modo escucha latente desde que se ejecuta el programa hasta que se termina, es importante aclarar que se aceptan conexión concurrentes gracias al manejo de hilos\\
    
    - conexionCliente : Método principal donde se va a interactuar con el cliente, este método va a corroborar los código correspondientes, también a a ofrecer los Pokemon que tiene disponibles, también esta al tanto de los timeouts. Esta función utiliza los métodos siguientes para interactuar con el cliente y los Pokemon  
    
    - img_bytes : Función auxiliar que convierte el tamaño de una imagen a bytes.
    
    - mandar_pokemon : Esta función permite obtener un Pokemon y ofrecerlo al cliente.
    
    - Es la función con la que vamos a intentar hacer que el cliente obtenga o no el Pokemon, también revisa los intentos, y si el cliente quiere seguir intentando capturar o no. 
    
