import socket
import sqlite3
from datetime import datetime

ARCHIVO_DB = 'chat.db'

def configurar_servidor(direccion='localhost', puerto=5000):
    """
    Inicializa el socket en TCP/IP y comienza a escuchar conexiones.
    """
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((direccion, puerto))
    srv.listen(5)
    print(f"Servidor corriendo en {direccion}:{puerto}")
    return srv


def guardar_en_db(texto, ip_cliente):
    """
    Guarda cada mensaje junto con fecha e IP en SQLite.
    """
    with sqlite3.connect(ARCHIVO_DB) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
            '''
        )
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            'INSERT INTO mensajes (texto, fecha_envio, ip_cliente) VALUES (?, ?, ?)',
            (texto, fecha, ip_cliente)
        )
        conexion.commit()


def atender_conexiones(servidor):
    """
    Acepta clientes y procesa sus mensajes en bucle.
    """
    while True:
        cliente_sock, addr = servidor.accept()
        print(f"Nueva conexión desde {addr}")
        try:
            while True:
                recibido = cliente_sock.recv(1024)
                if not recibido:
                    break
                mensaje = recibido.decode('utf-8')
                print(f"[{addr[0]}] {mensaje}")
                guardar_en_db(mensaje, addr[0])

                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                respuesta = f"Mensaje recibido: {ts}"
                cliente_sock.sendall(respuesta.encode('utf-8'))

        except Exception as ex:
            print(f"Error con {addr}: {ex}")
        finally:
            cliente_sock.close()
            print(f"Conexión cerrada {addr}")


if __name__ == '__main__':
    servidor = configurar_servidor()
    atender_conexiones(servidor)
