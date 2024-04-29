import socket, random
from udp_message import UdpMessage 

LOCALHOST = "127.0.0.1"
PORTA_CLIENTE = 8000
PORTA_SERVIDOR = 50000

class UdpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def start_client(self, host_server, port_server):
        
        while True:
        # Menu de opções

            print("\nSelecione o tipo de request que deseja fazer: ")
            print("0 - Data e Hora")
            print("1 - Mensagem Motivacional")
            print("2 - Quantidade de repostas emitidas até o momento")
            print("3 - Encerrar cliente")

            request_type = int(input("Digite o número correspondente ao tipo de request: "))


            if request_type == 3:
                print("Cliente encerrado")
                break

            # O identificador é um número aleatório de 1 a 65535 que mudará a cada request
            identifier = random.randint(1, 65535)


            # Cria a mensagem
            message = UdpMessage(1, request_type, identifier)

            print("\nMensagem criada: ", message)

            # Envia a mensagem
            self.send_udp_message(message.as_bytes(), host_server, port_server)

            print("Aguardando resposta...")

            print("Servidor criado para receber resposta: ", self.host, self.port)

            self.receive_udp_message(self.host, self.port)

            # Recebe a resposta

    def receive_udp_message(self, host, port):

        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        client_socket.bind((host, port))

        try: 

            message, _ = client_socket.recvfrom(4096)

            received_response = UdpMessage.from_bytes(message)


            received_is_request = int(received_response.is_request, 2)

            if received_is_request:
                raise Exception("Mensagem não é uma resposta")
            
            received_request_type = int(received_response.request_type, 2)

            if received_request_type == 3:
                raise Exception("Request foi julgado inválido pelo servidor")

            

            message = received_response.message.decode()

            print("\nResposta recebida: ", message)

        except Exception as e:
            print("\nErro ao receber resposta: ", e)
            

    def send_udp_message(self, message, host, port):

        # Cria um socket UDP
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.client_socket.bind((self.host, self.port))

        # Tenta enviar a mensagem
        try:
            self.client_socket.sendto(message, (host, port))
            print("\nMensagem enviada com sucesso")
        except Exception as e:
            print("\nErro ao enviar mensagem: ", e)
        finally:
            self.client_socket.close()



    
if __name__ == "__main__":

    client = UdpClient(LOCALHOST, PORTA_CLIENTE)
    client.start_client(LOCALHOST, PORTA_SERVIDOR)


 

   



