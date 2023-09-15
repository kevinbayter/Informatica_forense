import socket
import os
import datetime

LOG_FILE = "telnet_log.txt"

def log_event(event):
    """Función para registrar eventos en un archivo."""
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.datetime.now()} - {event}\n")

def list_active_processes():
    """Función para listar procesos activos."""
    processes = os.popen('ps aux').read()
    return processes

def list_active_connections():
    """Función para listar conexiones activas."""
    connections = os.popen('netstat -an').read()
    return connections

def start_telnet_server(port=23):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Servidor Telnet escuchando en el puerto {port}...")
    log_event(f"Servidor iniciado en el puerto {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión desde {client_address} establecida.")
        log_event(f"Conexión desde {client_address} establecida")

        welcome_message = "Bienvenido al servidor Telnet simulado.\n"
        welcome_message += "Escribe 'procesos' para ver los procesos activos.\n"
        welcome_message += "Escribe 'conexiones' para ver las conexiones activas.\n"
        welcome_message += "Escribe 'salir' para desconectarte.\n"
        client_socket.send(welcome_message.encode())

        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8').strip().lower()
            except UnicodeDecodeError:
                continue

            if data == "procesos":
                response = list_active_processes()
                client_socket.send(response.encode())
            elif data == "conexiones":
                response = list_active_connections()
                client_socket.send(response.encode())
            elif data == "salir":
                break
            else:
                message = "Comando no reconocido. Usa 'procesos', 'conexiones' o 'salir'.\n"
                client_socket.send(message.encode())

        client_socket.close()
        print(f"Conexión desde {client_address} cerrada.")
        log_event(f"Conexión desde {client_address} cerrada")

if __name__ == "__main__":
    start_telnet_server()
