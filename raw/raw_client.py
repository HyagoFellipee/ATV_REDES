import socket, random
from raw_message import RawMessage 
from udp_message import UdpMessage

class RawClient:
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
            identifier = 23777

            # Cria a mensagem
            message = RawMessage(0, request_type, identifier)


            # Adiciona o header IP e UDP
            message.set_udp_header(self.port, port_server, checksum=0)            
            message.set_ip_header(self.host, host_server)


            message.udp_header.checksum = message.udp_header.calculate_checksum(self.host, host_server, message.as_bytes()[28:])

            

            # Envia a mensagem como bytes
            self.send_raw_message(message.as_bytes(), host_server, port_server)

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

        # seta um timeout para o socket
        client_socket.settimeout(5)
            
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
        
            

    def send_raw_message(self, message, dest_host, dest_port):
        '''
        Envia uma mensagem para o servidor
        message: Mensagem a ser enviada
        dest_host: IP do servidor
        dest_port: Porta do servidor
        '''

        # Cria um socket do tipo raw
        # AF_INET indica que é um endereço IP
        # SOCK_RAW indica que é um socket do tipo raw
        # IPPROTO_RAW indica que é um protocolo raw

        client_raw_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_RAW)
        client_raw_socket.bind((self.host, self.port))

        # Habilita o cabeçalho IP
        client_raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Envia a mensagem
        client_raw_socket.sendto(message, (dest_host, dest_port))

        client_raw_socket.close()




    


 

   



