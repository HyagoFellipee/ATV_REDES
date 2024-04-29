import socket, random, os
from dotenv import load_dotenv
from udp_message import UdpMessage 



def send_udp_message(message, host, port):

    # Cria um socket UDP
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Tenta enviar a mensagem
    try:
        client_socket.sendto(message, (host, port))
        print("\nMensagem enviada com sucesso")
    except Exception as e:
        print("\nErro ao enviar mensagem: ", e)
    finally:
        client_socket.close()



    
if __name__ == "__main__":



    # Iniciando o cliente
    load_dotenv()
    LOCALHOST = os.getenv("LOCALHOST")
    PORTA_SERVIDOR = int(os.getenv("PORTA_SERVIDOR"))

    while True:
        # Menu de opções

        print("\nSelecione o tipo de request que deseja fazer: ")
        print("1 - Data e Hora")
        print("2 - Mensagem Motivacional")
        print("3 - Quantidade de repostas emitidas até o momento")
        print("4 - Encerrar servidor")

        request_type = int(input("Digite o número correspondente ao tipo de request: "))

        if request_type == 4:
            print("Cliente encerrado")
            break

        # O identificador é um número aleatório de 1 a 65535 que mudará a cada request
        identifier = random.randint(1, 65535)

        # Cria a mensagem
        message = UdpMessage(0, request_type, identifier)

        # Envia a mensagem
        send_udp_message(message.as_bytes(), LOCALHOST, PORTA_SERVIDOR)



