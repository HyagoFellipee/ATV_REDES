import socket, datetime, random
from raw_message import RawMessage

IP_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 50000


class RawServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.frases_motivacionais = [
            "Você está mais perto do que imagina. Continue persistindo!",
            "Cada desafio que você enfrenta é uma oportunidade para crescer.",
            "Confie no seu potencial. Você é capaz de alcançar grandes feitos!",
            "O sucesso não é definitivo, o fracasso não é fatal: é a coragem de continuar que conta.",
            "Não se compare aos outros. Sua jornada é única e especial.",
            "Você já superou tantos obstáculos, este não será diferente!",
            "Lembre-se do motivo pelo qual começou. Mantenha o foco!",
            "Seu esforço será recompensado. Continue trabalhando duro!",
            "Cada pequena vitória é um passo em direção ao seu objetivo final.",
            "O importante é não desistir. A perseverança é a chave do sucesso!",
            "Acredite no seu potencial. Você é mais forte do que pensa!",
            "O sucesso não é uma linha reta. Aprenda com os desafios e siga em frente!",
            "Você está aprendendo e crescendo a cada dia. Valorize cada passo do seu progresso!",
            "Lembre-se: a jornada é tão importante quanto o destino final.",
            "Celebre suas conquistas, por menores que sejam. Cada uma delas é significativa!",
            "Mantenha a mente positiva e os resultados virão!",
            "Você é capaz de transformar desafios em oportunidades.",
            "A persistência é o caminho do êxito. Continue persistindo!",
            "Acredite na sua capacidade de superar qualquer obstáculo!",
            "Não deixe que o cansaço tome conta. Você está mais próximo do que imagina!",
        ]
        self.request_counter = 0

    def start_server(self):
        while True:

            response, address = self.receive_raw_message(self.host, self.port)

            client_host = address[0]
            client_port = address[1]

            self.send_raw_message(response, client_host, client_port)



    def receive_raw_message(self,host, port):
        
            # Cria um socket UDP
            server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
            # Faz o bind do socket
            server_socket.bind((host, port))

            print("Servidor esperando messagem em ", host, ":", port)
        
            # Tenta receber a mensagem
            try:
                message, address = server_socket.recvfrom(4096)
                print("Mensagem recebida: ", message, " de ", address)

                self.request_counter += 1

                # Decodifica a mensagem, ela vem como um hexadecimal do tipo b'\x007Q'

                received_response = RawMessage.from_bytes(message)

                received_is_request = int(received_response.is_request, 2)
                received_request_type = int(received_response.request_type, 2)
                received_identifier = int(received_response.identifier, 2)

                if not received_is_request:
                    raise Exception("Mensagem não é um request")



                if received_request_type == 0:
                    print("Request de data e hora")
                    response_message = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                elif received_request_type == 1:
                    print("Request de mensagem motivacional")
                    response_message = random.choice(self.frases_motivacionais)
                elif received_request_type == 2:
                    print("Request de quantidade de respostas emitidas")
                    response_message = "Quantidade de respostas emitidas: " + str(self.request_counter)

                response_is_request = 0
                response_request_type = received_request_type
                response_identifier = received_identifier


                response = RawMessage(response_is_request, response_request_type, response_identifier, len(response_message), response_message)

                return response, address
            
            except Exception as e:
                print("Erro ao receber mensagem: ", e)

                response_is_request = 0
                response_request_type = 3
                response_identifier = 0

                response = RawMessage(response_is_request, response_request_type, response_identifier)

                return response, address
    
    def send_raw_message(self, message, dest_host, dest_port):

        # Cria um socket RAW
        self.server_raw_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_RAW)
        self.server_raw_socket.bind((self.host, self.port))

        message.set_udp_header(self.port, dest_port, checksum=0)
        message.set_ip_header(self.host, dest_host)


        # Tenta enviar a mensagem
        try:
            self.server_raw_socket.sendto(message.as_bytes(), (dest_host, dest_port))
            print("Mensagem enviada com sucesso para ", dest_host, ":", dest_port)
        except Exception as e:
            print("Erro ao enviar mensagem: ", e)
        finally:
            self.server_raw_socket.close()

if __name__ == "__main__":

    # Iniciando o servidor
    server = RawServer(IP_SERVIDOR, PORTA_SERVIDOR)
    server.start_server()