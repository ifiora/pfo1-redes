import socket

# Inicia el cliente
def iniciar_cliente(host='localhost', puerto=5000):
    """
    Conecta al servidor, envía mensajes hasta que el usuario teclee 'exito'
    y muestra la respuesta que llega de vuelta.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Se conecta al servidor usando el puerto e IP correspondiente
        cliente.connect((host, puerto))
        print(f"Conectado a {host}:{puerto}")

        while True:
            texto = input("Ingresa un mensaje (o 'exito' para terminar): ")
            if texto.strip().lower() == 'exito':
                print("Terminando cliente...")
                break

            
            cliente.sendall(texto.encode('utf-8'))
            datos = cliente.recv(2048)
            print(f"Respuesta del servidor: {datos.decode('utf-8')}")

    except ConnectionRefusedError:
        print("No se pudo conectar. ¿El servidor está activo?")
    except Exception as err:
        print(f"Error en el cliente: {err}")
    finally:
        cliente.close()


if __name__ == '__main__':
    iniciar_cliente()
