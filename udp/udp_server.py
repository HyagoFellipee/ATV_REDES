import socket, datetime, os
from dotenv import load_dotenv
from udp_message import UdpMessage




def receive_udp_message(host, port):
    
        # Cria um socket UDP
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
        # Faz o bind do socket
        server_socket.bind((host, port))

        print("Servidor iniciado em ", host, ":", port)
    
        # Tenta receber a mensagem
        try:
            message, address = server_socket.recvfrom(4096)
            print("Mensagem recebida: ", message, " de ", address)

            # Decodifica a mensagem	
            message = message.decode()
            print("Mensagem decodificada: ", message)

        except Exception as e:
            print("Erro ao receber mensagem: ", e)



if __name__ == "__main__":
    # Iniciando o servidor
    # 
    load_dotenv()
    localhost = os.getenv("LOCALHOST")
    port = int(os.getenv("PORTA_SERVIDOR"))


    while True:
        receive_udp_message(localhost, port)