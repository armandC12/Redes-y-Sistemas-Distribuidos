# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
import os
import base64
from constants import *

class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        # Inicializar atributos de Connection
        self.socket = socket
        self.directory = directory

    def handle(self):
        try:
            while True:
                # Esperar un comando del cliente
                command = self.socket.recv(1024).decode("ascii").strip()

                # Separar comandos
                commands = command.split('\r\n')

                # Procesar cada comando individualmente
                for cmd in commands:
                    # Separar comando y argumentos
                    parts = cmd.split(" ")
                    command_name = parts[0]
                    args = parts[1:]

                    # Manejar comandos
                    if command_name == "get_file_listing":
                        if len(args) != 0:
                            response = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
                        else:
                            response = self.get_file_listing()
                    elif command_name == "get_metadata":
                        if len(args) != 1:
                            response = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
                        else:
                            filename = args[0]
                            response = self.get_metadata(filename)
                    elif command_name == "get_slice":
                        if len(args) != 3:
                            response = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
                        else:
                            filename = args[0]
                            offset = args[1]
                            size = args[2]
                            response = self.get_slice(filename, offset, size)
                    elif command_name == "quit":
                        if len(args) != 0:
                            response = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
                        else:
                            response = f"{CODE_OK} {error_messages[CODE_OK]}{EOL}"
                            self.socket.send(response.encode("ascii"))
                            self.socket.close()
                            break
                    else:
                        response = f"{INVALID_COMMAND} {error_messages[INVALID_COMMAND]}{EOL}"

                    # Enviar respuesta al cliente
                    self.socket.send(response.encode("ascii"))

        except Exception:
            pass

        finally:
            # Cerrar la conexión
            self.socket.close()


    def get_file_listing(self):
        try:
            files = os.listdir(self.directory)
            response = f"{CODE_OK} {error_messages[CODE_OK]}{EOL}"
            for file in files:
                response += file + EOL
            response += EOL
            return response
        except OSError:
            return f"{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}{EOL}"

    def get_metadata(self, filename):
        try:
            filepath = os.path.join(self.directory, filename)
            if not os.path.exists(filepath):
                return f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
            size = os.path.getsize(filepath)
            return f"{CODE_OK} {error_messages[CODE_OK]}{EOL}{size}{EOL}"
        except OSError:
            return f"{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}{EOL}"

    def get_slice(self, filename, offset, size):
        if not str.isnumeric(offset) or not str.isnumeric(size):
             return f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
        try:
            offset = int(offset)
            size = int(size)
            filepath = os.path.join(self.directory, filename)
            if not os.path.exists(filepath):
                return f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
            filesize = os.path.getsize(filepath)
            if offset >= filesize:
                return f"{BAD_OFFSET} {error_messages[BAD_OFFSET]}{EOL}"
            with open(filepath, "rb") as f:
                f.seek(offset)
                data = f.read(min(size, filesize - offset))
                encoded_data = base64.b64encode(data).decode("ascii")
                return f"{CODE_OK} {error_messages[CODE_OK]}{EOL}{encoded_data}{EOL}"
        except OSError:
            return f"{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}{EOL}"
