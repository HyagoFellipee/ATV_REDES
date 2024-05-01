import socket, random
from udp_message import UdpMessage 

class UdpClient:
    def __init__(self, host, port):
        '''
        Inicializa o cliente UDP
        host: IP do cliente
        port: Porta do cliente
        '''

        self.host = host
        self.port = port


    def start_client(self, host_server, port_server):
        ''' 
        Inicia o cliente UDP 
        host_server: IP do servidor
        port_server: Porta do servidor
        '''

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

            # Envia a mensagem como bytes
            self.send_udp_message(message.as_bytes(), host_server, port_server)

            print("Aguardando resposta...")

            # Recebe a resposta
            self.receive_udp_message()


    def receive_udp_message(self):
        '''
        Inicia o servidor UDP para receber a resposta do servidor
        '''

        # Cria o socket do tipo UDP
        # AF_INET indica que é um endereço IP
        # SOCK_DGRAM indica que é um socket do tipo UDP

        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


        # Associa o socket ao endereço e porta do cliente
        client_socket.bind((self.host, self.port))
            
        # Cria um buffer para receber a mensagem
        message, _ = client_socket.recvfrom(4096)

        # Converte a mensagem recebida em um objeto UdpMessage
        received_response = UdpMessage.from_bytes(message)


        received_is_response = int(received_response.is_response)

        if not received_is_response:
            raise Exception("Mensagem não é uma resposta")
        
        received_request_type = int(received_response.request_type)

        if received_request_type == 3:
            raise Exception("Request foi julgado inválido pelo servidor")

        

        message = received_response.message.decode()

        print("\nResposta recebida: ", message)


    def send_udp_message(self, message, host, port):
        '''
        Envia uma mensagem para o servidor
        message: Mensagem a ser enviada
        host: IP do servidor
        port: Porta do servidor
        '''

        # Cria o socket do tipo UDP
        # AF_INET indica que é um endereço IP
        # SOCK_DGRAM indica que é um socket do tipo UDP

        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        # Associa o socket ao endereço e porta do cliente, necesário para receber a resposta
        client_socket.bind((self.host, self.port))
        
        # Envia a mensagem para o servidor
        client_socket.sendto(message, (host, port))
        client_socket.close()
    
