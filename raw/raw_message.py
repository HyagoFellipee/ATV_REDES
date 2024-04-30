import struct

class RawMessage: 
    def __init__(self, is_request, request_type, identifier, message_length=0, message=""):
        
        self.is_request     = bin(is_request)[2:].zfill(4) # 4 bits
        self.request_type   = bin(request_type)[2:].zfill(4) # 4 bits 
        self.identifier     = bin(identifier)[2:].zfill(16) # 16 bits
        self.message_length = bin(message_length)[2:].zfill(8) # 8 bits
        self.message        = message.encode() # depende de message_length

        self.udp_header = UdpHeader()
        self.ip_header = IpHeader()


        self.control_bytes_list = [self.is_request + self.request_type, self.identifier[:8], self.identifier[8:]]

        self.bytes_list = self.control_bytes_list.copy()

        if message_length:
            self.bytes_list.append(self.message_length)
            for byte in self.message:
                self.bytes_list.append(bin(byte)[2:].zfill(8))

        self.whole_binary = "".join(self.bytes_list)

    def binary(self):
        return self.whole_binary
    
    def set_udp_header(self, orig_port, dest_port, checksum):
        udp_header_len = 8
        self.udp_header = UdpHeader(orig_port, dest_port, len(self.bytes_list) + udp_header_len, checksum)

        udp_binary_bytes_list = [bin(byte)[2:].zfill(8) for byte in self.udp_header.as_bytes()]
        self.bytes_list = udp_binary_bytes_list + self.bytes_list

    def set_ip_header(self, source_address, dest_address):
        
        if self.udp_header.orig_port == 0 or self.udp_header.dest_port == 0:
            raise Exception("UDP Header não foi setado")
        
        ip_header_len = 20
        self.ip_header = IpHeader(
            header_length=5, # header len representa o número de palavras de 32 bits
            total_length=len(self.bytes_list) + ip_header_len,
            time_to_live=64, # Acredito que seja mais que suficiente
            source_address=source_address,
            dest_address=dest_address
        )

        ip_binary_bytes_list = [bin(byte)[2:].zfill(8) for byte in self.ip_header.as_bytes()]
        
        self.bytes_list = ip_binary_bytes_list + self.bytes_list
        
    def as_bytes(self):
        return bytes([int(byte, 2) for byte in self.bytes_list])
    
    def from_bytes(bytes_message):

        # uso format para converter os bytes em binário e não perder os zeros à esquerda

        binary_message = ''.join(format(byte, '08b') for byte in bytes_message)

        is_request = int(binary_message[:4], 2)
        request_type = int(binary_message[4:8], 2)
        identifier = int(binary_message[8:24], 2)
        message_length = int(binary_message[24:32], 2) if len(binary_message) > 32 else 0

        message = bytes_message[4:].decode() if message_length else ""


        return RawMessage(is_request, request_type, identifier, message_length, message)

    def __str__(self):


        message = ""

        # Header como hexadecimal
        for byte in self.control_bytes_list:
            message += str(hex(int(byte, 2))) + " "

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
        
        self.orig_port = orig_port
        self.dest_port = dest_port
        self.length = length
        self.checksum = checksum

    def as_bytes(self):

        # struct.pack converte os valores para bytes dado um formato e uma lista de valores
        # ! indica que é big-endian, que é o formato de rede mais comum
        # H indica que é um unsigned short (2 bytes)
        # 4H indica que são 4 unsigned shorts

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
        # ! indica que é big-endian, que é o formato de rede mais comum
        # B indica que é um unsigned char (1 byte)
        # H indica que é um unsigned short (2 bytes)
        # 4s indica que são 4 unsigned chars (4 bytes)

        version_and_header_length = (self.version << 4) + self.header_length
        flags_and_fragment_offset = (self.flags << 13) + self.fragment_offset

        # s tem que ser do tipo byte, e está como uma string representando um endereço IP

        dest_address_as_byte = bytes(map(int, self.dest_address.split('.')))
        source_address_as_byte = bytes(map(int, self.source_address.split('.')))


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
                 

    