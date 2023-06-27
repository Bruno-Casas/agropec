import socket
from io import BytesIO
import threading
import logging
import webview.handshake_pb2 as handshake_pb2
from diskcache import Cache

logging.basicConfig(level=logging.DEBUG)

cache = Cache('/tmp/diskcache')
#cache.close()
logging.info(f'Cache setup value: {cache.get("cache")}')
logging.info('--------------')

SECRET = 'TesteSecret'

CLIENT_BUFFER=1024

def watch(data, addr):  
    hand_shake = handshake_pb2.HandShake()
    hand_shake.ParseFromString(data)

    logging.info(f'{addr} Message received (broadcast): {hand_shake.port}')
    logging.info(f'{addr} Starting negotiation process')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((addr[0], hand_shake.port))
    
    sock.sendall(b'Isso o um teste\x17')

    try: 
        data = BytesIO()
        chunk: bytes
        while True:
            chunk = sock.recv(CLIENT_BUFFER)
            if chunk.endswith(b'\x17') or not chunk:
                data.write(chunk[0:-1])
                break
            else:
                data.write(chunk)
        
        logging.info(f'{addr} Message received (TCP): {data.getvalue()}')
    except socket.error as e:
        logging.error(f'Socket error: {e}')
    except Exception as e: 
        logging.error(f'Other Socket error: {e}')
    finally: 
        sock.close()
        logging.info(f'{addr} Negotiation process stopped')


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))

import signal

run = True
def create_handler(socket):
    def _handler(signum, frame):
        logging.info('Monitoring of tcp messages stopped')
        socket.close()

    return _handler

signal.signal(signal.SIGINT, create_handler(client))

while True:
    logging.info('Listening to broadcast messages...')
    try:   
        resp = client.recvfrom(1024)
        tcp = threading.Thread(target=watch, args=resp) 
        tcp.start()
    except (OSError):
        break
