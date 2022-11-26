# --- 소켓 통신 모듈 --- #
from socket import AF_INET, SOCK_STREAM, socket
import pickle

PORT = 26656
PACKET_SIZE = 256

# TCP 통신을 수행하는 클래스입니다.
# 데이터의 송수신은 다음과 같은 과정으로 진행됩니다.
# 1. 먼저 보낼 데이터의 크기를 보낸다.
# 2. 데이터를 pickle 모듈의 dumps 함수를 사용해 bytes 타입으로 직렬화한다.
# 3. 직렬화한 데이터를 packetSize 만큼 잘라서 보낸다.
class TcpClient:
    def __init__(self, ip: str, port: int = PORT):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((ip, port))

    # 데이터를 수신합니다.
    def getData(self, packetSize: int = PACKET_SIZE):
        packet = b''

        dataSize = int.from_bytes(self.sock.recv(packetSize))

        while dataSize > 0:
            packet += self.sock.recv(min(dataSize, packetSize))
            dataSize -= packetSize

        return pickle.loads(packet)

    # 데이터를 송신합니다.
    def sendData(self, data, packetSize: int = PACKET_SIZE):
        packet = pickle.dumps(data)

        self.sock.send(len(packet).to_bytes(packetSize))
        while packet:
            self.sock.send(packet[:packetSize])
            packet = packet[packetSize:]
