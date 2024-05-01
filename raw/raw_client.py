import socket, random
from raw_message import RawMessage 

MEU_IP = socket.gethostbyname(socket.gethostname())
IP_SERVIDOR = "15.228.191.109"

PORTA_CLIENTE = 8000
PORTA_SERVIDOR = 50000

class RawClient:
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
            message = RawMessage(0, request_type, identifier)

            print("\nMensagem criada: ", message)

            # Envia a mensagem
            self.send_raw_message(message, host_server, port_server)

            print("Aguardando resposta...")

            print("Servidor criado para receber resposta: ", self.host, self.port)

            self.receive_raw_message()

            # Recebe a resposta

    def receive_raw_message(self):

        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        client_socket.bind((self.host, self.port))

        try: 
            print("Servidor criado para receber resposta: ", self.host, self.port)
            message, _ = client_socket.recvfrom(4096)

            received_response = RawMessage.from_bytes(message)


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

        
            

    def send_raw_message(self, message, dest_host, dest_port):

        # Cria um socket RAW
        client_raw_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_RAW)
        client_raw_socket.bind((self.host, self.port))

        message.set_udp_header(self.port, dest_port, checksum=0)
        message.set_ip_header(self.host, dest_host)

      
        client_raw_socket.sendto(message.as_bytes(), (dest_host, dest_port))
    
        client_raw_socket.close()



    


 

   



