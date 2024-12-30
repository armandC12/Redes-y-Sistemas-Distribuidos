#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import connection
from constants import *
import sys

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))
        # Creamos socket del servidor, configuramos, asignamos
        # a una dirección y puerto, etc.
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Asociaciamos el conector con la direccion del servidor.
        self.s.bind((addr, port))
        # Inicia la escucha, habilita nuevos hilos de C-S hasta 1 veces en simultaneo
        self.s.listen(1)
        # Asignamos el directorio dado
        self.directory = directory
        # Ahora el conector esta en modo servidor

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        while True:
            # Aceptar una conexión al server, crear una
            # Connection para la conexión y atenderla hasta que termine.
        
            # Devuelve un socket 'c' y una direccion destino 'a'.
            print ("Wainting for a connection")
            conexion,address = self.s.accept() # Aceptamo al cliente TCP
            print("Conexion establecida!!")
            
            c = connection.Connection(conexion, self.directory)
            c.handle()
            

def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)
        
    datadir = options.datadir   # Acceder al valor de "-d"
    port = int(options.port)    # Accede al puerto
    server = Server(options.address, port, datadir)
    server.serve()

if __name__ == '__main__':
    main()