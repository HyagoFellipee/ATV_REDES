import struct


class UdpMessage: 
    def __init__(self, is_response, request_type, identifier, message_length=0, message=""):
        '''
        Inicializa a mensagem UDP
        is_response: indica se é uma resposta
        request_type: tipo da requisição
        identifier: identificador da mensagem
        message_length: tamanho da mensagem
        message: mensagem
        '''

        self.is_response    = is_response       # 4 bits
        self.request_type   = request_type      # 4 bits 
        self.identifier     = identifier        # 16 bits
        self.message_length = message_length    # 8 bits
        self.message        = message.encode()  # depende do message_length

        
    def as_bytes(self):
        '''
        Converte a mensagem em bytes
        '''

        # struct.pack converte os valores em bytes dado um formato e uma lista de valores
        # ! indica que a ordem dos bytes é big-endian, que é o formato de rede mais comum
        # B indica que é um unsigned char (1 byte)
        # H indica que é um unsigned short (2 bytes)

        is_response_and_request_type = (self.is_response << 4) + self.request_type

        header = struct.pack('!BHB', is_response_and_request_type, self.identifier, self.message_length)
        
        return header + self.message
    
    def from_bytes(bytes_message):
        '''
        Converte bytes para uma mensagem
        bytes_message: bytes da mensagem
        '''

        # struct.unpack converte os bytes em valores dado um formato e uma lista de bytes
        # ! indica que a ordem dos bytes é big-endian, que é o formato de rede mais comum
        # B indica que é um unsigned char (1 byte)
        # H indica que é um unsigned short (2 bytes)

        is_response_and_request_type, identifier, message_length = struct.unpack('!BHB', bytes_message[:4])

        is_response = is_response_and_request_type >> 4 # shift para pegar os 4 bits mais significativos
        request_type = is_response_and_request_type & 0b00001111 # mascara para pegar os 4 bits menos significativos


        # Se a mensagem existe, verifica se é um número ou uma string pela request_type
        # Se for um número, converte para string
        # Se for uma string, decodifica para UTF-8

        if message_length:
            if request_type == 2:
                message = str(int.from_bytes(bytes_message[4:], byteorder='big'))
            else:
                message = bytes_message[4:].decode()
        else: 
            message = ""


        return UdpMessage(is_response, request_type, identifier, message_length, message)

