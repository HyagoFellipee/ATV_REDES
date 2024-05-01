import socket, random
from udp_message import UdpMessage 

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
            message = UdpMessage(0, request_type, identifier)

            print("\nMensagem criada: ", message)

            # Envia a mensagem
            self.send_udp_message(message.as_bytes(), host_server, port_server)

            print("Aguardando resposta...")


            self.receive_udp_message()

            # Recebe a resposta

    def receive_udp_message(self):

        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        client_socket.bind((self.host, self.port))

        try: 
            
            print("Servidor criado para receber resposta: ", self.host, self.port)
            message, _ = client_socket.recvfrom(4096)


            received_response = UdpMessage.from_bytes(message)


            received_is_response = int(received_response.is_response, 2)

            if not received_is_response:
                raise Exception("Mensagem não é uma resposta")
            
            received_request_type = int(received_response.request_type, 2)

            if received_request_type == 3:
                raise Exception("Request foi julgado inválido pelo servidor")

            
    
            message = received_response.message.decode()

            print("\nResposta recebida: ", message)

        except Exception as e:
            print("\nErro ao receber resposta: ", e)
            

    def send_udp_message(self, message, host, port):
     
        # Create a UDP socket
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        client_socket.bind((self.host, self.port))
        
        # Attempt to send the message
        client_socket.sendto(message, (host, port))
        client_socket.close()
    
