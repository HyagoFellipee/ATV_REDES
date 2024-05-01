from udp_client import UdpClient
import socket



    
if __name__ == "__main__":

    MEU_IP = socket.gethostbyname(socket.gethostname())
    IP_SERVIDOR = "15.228.191.109"

    PORTA_CLIENTE = 8000
    PORTA_SERVIDOR = 50000

    client = UdpClient(MEU_IP, PORTA_CLIENTE)
    client.start_client(IP_SERVIDOR, PORTA_SERVIDOR)


 

   



