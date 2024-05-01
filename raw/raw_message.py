import struct

class RawMessage: 
    def __init__(self, is_response, request_type, identifier, message_length=0, message=""):
        '''
        Inicializa uma mensagem raw
        is_response: se é uma resposta
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

        self.udp_header = UdpHeader()
        self.ip_header = IpHeader()


    
    def set_udp_header(self, orig_port, dest_port, checksum):
        '''
        Seta o header UDP da mensagem
        orig_port: porta de origem
        dest_port: porta de destino
        checksum: checksum do header
        '''
        
        udp_header_len = 8
        data_header_len = 4
        data_len = self.message_length

        segment_len = udp_header_len + data_header_len + data_len

        self.udp_header = UdpHeader(orig_port, dest_port, segment_len, checksum)


    def set_ip_header(self, source_address, dest_address):
        '''
        Seta o header IP da mensagem
        source_address: endereço de origem
        dest_address: endereço de destino
        '''
        
        if self.udp_header.orig_port == 0 or self.udp_header.dest_port == 0:
            raise Exception("UDP Header não foi setado")
        
        udp_header_len = 8
        data_header_len = 4
        data_len = self.message_length

        segment_len = udp_header_len + data_header_len + data_len

        ip_header_len = 20

        packet_len = segment_len + ip_header_len


        self.ip_header = IpHeader(
            header_length=5, # header len representa o número de palavras de 32 bits
            total_length=packet_len,
            time_to_live=64, # Acredito que seja suficiente 
            source_address=source_address,
            dest_address=dest_address
        )

        
    def as_bytes(self):
        '''
        Converte a mensagem para bytes
        '''

        # struct.pack converte os valores em bytes dado um formato e uma lista de valores
        # ! indica que a ordem dos bytes é big-endian, que é o formato de rede mais comum
        # B indica que é um unsigned char (1 byte)
        # H indica que é um unsigned short (2 bytes)

        is_response_and_request_type = (self.is_response << 4) + self.request_type

        header = struct.pack('!BHB', is_response_and_request_type, self.identifier, self.message_length)

        data = header + self.message
        segment = self.udp_header.as_bytes() + data
        packet = self.ip_header.as_bytes() + segment

        return packet
    

    def from_bytes(bytes_message):
        '''
        Converte bytes para uma mensagem
        bytes_message: bytes da mensagem
        '''

        # IMPORTANTE: Como o servidor utilizado para
        # receber as mensagens é um servidor UDP, 
        # e não um RAW, não é preciso tratar o header IP e UDP

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

        return RawMessage(is_response, request_type, identifier, message_length, message)

    def __str__(self):
        '''
        Formata a mensagem para exibição, apenas para facilitar a visualização
        '''

        message = ""
        
        ip_header_len = self.ip_header.header_length * 4
        udp_header_len = self.udp_header.length
        data_header_len = 4

        total_header_len = ip_header_len + udp_header_len + data_header_len + self.message_length

        # Header como hexadecimal
        for byte in self.as_bytes()[0:total_header_len]:
            message += str(hex(byte)) + " "

        # Mensagem como caracteres
        for byte in self.message:
            message += chr(byte)        

            
        return message
    


class UdpHeader: 
    def __init__(
            self,
            orig_port = 0, 
            dest_port = 0, 
            length = 0, 
            checksum = 0
    ):
        '''
        Inicializa o header UDP
        orig_port: porta de origem
        dest_port: porta de destino
        length: tamanho do segmento
        checksum: checksum do header
        '''
        
        self.orig_port = orig_port
        self.dest_port = dest_port
        self.length = length
        self.checksum = checksum

    def as_bytes(self):
        '''
        Converte o header para bytes
        '''

        # struct.pack converte os valores para bytes dado um formato e uma lista de valores
        # ! indica que é big-endian, que é o formato de rede mais comum
        # H indica que é um unsigned short (2 bytes)

        return struct.pack("!HHHH", self.orig_port, self.dest_port, self.length, self.checksum)


class IpHeader: 
    def __init__(
            self, 
            header_length=0,
            type_of_service=0,
            total_length=0,
            identification=0,
            flags=0,
            fragment_offset=0,
            time_to_live=0,
            source_address=0,
            header_checksum=0,
            dest_address=0,
            version=4, # IPv4
            upper_layer_protocol=17, # UDP
            options=None
    ): 
        '''
        Inicializa o header IP
        header_length: tamanho do header em palavras de 32 bits
        type_of_service: tipo de serviço
        total_length: tamanho do pacote
        identification: identificação do pacote
        flags: flags do pacote
        fragment_offset: offset do fragmento
        time_to_live: tempo de vida do pacote
        source_address: endereço de origem
        header_checksum: checksum do header
        dest_address: endereço de destino
        version: versão do IP
        upper_layer_protocol: protocolo da camada superior
        options: opções do header
        '''
        
        self.version = version
        self.header_length = header_length
        self.type_of_service = type_of_service
        self.total_length = total_length
        self.identification = identification
        self.flags = flags
        self.fragment_offset = fragment_offset
        self.time_to_live = time_to_live
        self.upper_layer_protocol = upper_layer_protocol
        self.header_checksum = header_checksum
        self.source_address = source_address
        self.dest_address = dest_address
        self.options = options

    def as_bytes(self):
        '''
        Converte o header para bytes
        '''

        # ! indica que é big-endian, que é o formato de rede mais comum
        # B indica que é um unsigned char (1 byte)
        # H indica que é um unsigned short (2 bytes)
        # 4s indica que são 4 unsigned chars (4 bytes)

        version_and_header_length = (self.version << 4) + self.header_length
        flags_and_fragment_offset = (self.flags << 13) + self.fragment_offset

        # s tem que ser do tipo byte, e está como uma string representando um endereço IP
        # Para cada número do endereço IP, converte para inteiro e depois para byte
        source_address_as_byte = bytes(map(int, self.source_address.split('.'))) if isinstance(self.source_address, str) else self.source_address
        dest_address_as_byte = bytes(map(int, self.dest_address.split('.'))) if isinstance(self.dest_address, str) else self.dest_address


        return struct.pack("!BBHHHBBH4s4s",
            version_and_header_length, # 8 bits
            self.type_of_service, # 8 bits
            self.total_length, # 16 bits
            self.identification, # 16 bits
            flags_and_fragment_offset, # 16 bits
            self.time_to_live, # 8 bits
            self.upper_layer_protocol, # 8 bits
            self.header_checksum, # 16 bits 
            source_address_as_byte, # 32 bits
            dest_address_as_byte # 32 bits
        )
                 

    