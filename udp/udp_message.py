class UdpMessage: 
    def __init__(self, is_request, request_type, identifier, message_length=0, message=""):
        
        self.is_request     = bin(is_request)[2:].zfill(4) # 4 bits
        self.request_type   = bin(request_type)[2:].zfill(4) # 4 bits 
        self.identifier     = bin(identifier)[2:].zfill(16) # 16 bits
        self.message_length = bin(message_length)[2:].zfill(8) # 8 bits
        self.message        = message.encode() # depende de message_length

        self.header_bytes_list = [self.is_request + self.request_type, self.identifier[:8], self.identifier[8:]]

        self.bytes_list = self.header_bytes_list.copy()

        if message_length:
            self.bytes_list.append(self.message_length)
            for byte in self.message:
                self.bytes_list.append(bin(byte)[2:].zfill(8))

        self.whole_binary = "".join(self.bytes_list)

    def binary(self):
        return self.whole_binary

        
    def as_bytes(self):

        return bytes([int(byte, 2) for byte in self.bytes_list])
    
    def from_bytes(bytes_message):

        binary_message = ''.join(format(byte, '08b') for byte in bytes_message)

        is_request = int(binary_message[:4], 2)
        request_type = int(binary_message[4:8], 2)
        identifier = int(binary_message[8:24], 2)
        message_length = int(binary_message[24:32], 2) if len(binary_message) > 32 else 0

        message = bytes_message[4:].decode() if message_length else ""


        return UdpMessage(is_request, request_type, identifier, message_length, message)

    def __str__(self):


        message = ""

        # Header como hexadecimal
        for byte in self.header_bytes_list:
            message += str(hex(int(byte, 2))) + " "

        # Mensagem como caracteres
        for byte in self.message:
            message += chr(byte)        

            
        return message
