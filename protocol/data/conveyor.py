from io import BytesIO
import json
import socket
import threading
import logging
import handshake_pb2 as handshake_pb2
from diskcache import Cache
import urllib.request
import time
import signal
import sys

logging.basicConfig(level=logging.DEBUG)

cache = Cache('/tmp/diskcache')
# cache.close()
logging.info(f'Cache setup value: {cache.get("cache")}')
logging.info(' --------------')

SECRET = 'TesteSecret'
CLIENT_BUFFER = 1024

stop_event = threading.Event()
send_broadcast = threading.Event()

def setup_tcp_socket():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    return tcp

def setup_udp_socket():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    return udp

def udp_service(udp_socket, tcp_server_port):
    host_ip = socket.gethostbyname(socket.gethostname())
    
    def udp_connection(data, addr):
        hand_shake = handshake_pb2.HandShake()
        hand_shake.ParseFromString(data)

        logging.info(f'{addr} Message received (broadcast): {hand_shake.port}')
        logging.info(f'{addr} Starting negotiation process')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((addr[0], hand_shake.port))

        sock.sendall((cache.get('cache') or b'') + b'\x17')

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
            
            cache.close()
            with Cache(cache.directory) as reference:
                if data.getvalue():
                    reference.set('cache', data.getvalue())
            
        except socket.error as e:
            logging.error(f'Socket error: {e}')
        except Exception as e:
            logging.error(f'Other Socket error: {e}')
        finally:
            sock.close()
            logging.info(f'{addr} Negotiation process stopped')
    
    def server(socket_):
        port = 37020
        while True:
            try:
                socket_.bind(('', port))
                break
            except (Exception,):
                port += 1
                pass
        
        logging.info(' UDP server started in port ' + str(port))
        while (not stop_event.is_set()):
            resp = socket_.recvfrom(1024)
            if resp[1] and (resp[1][1] != port or resp[1][0] != host_ip):
                udp_connection(*resp)

    def client(socket_):
        hand_shake = handshake_pb2.HandShake()
        hand_shake.port = tcp_server_port
    
        logging.info(' UDP client is ready')
        while (not stop_event.is_set()):
            is_send = send_broadcast.wait() and not stop_event.is_set()
            if (is_send):
                for port in range(37020, 37023):
                    logging.info(' Sending UDP broadcast message to port ' + str(port))
                    socket_.sendto(hand_shake.SerializeToString(), ('<broadcast>', port))
                send_broadcast.clear()

    server_thread = threading.Thread(target=server, args=(udp_socket,))
    server_thread.start()

    client_thread = threading.Thread(target=client, args=(udp_socket,))
    #client_thread.start()

    thread_list.extend([server_thread, client_thread])

def tcp_server(tcp_socket) -> int:
    
    def tcp_connection(con, client):
        logging.info(f'{client} New connection')

        con.sendall((cache.get('cache') or b'') + b'\x17')

        try:
            data = BytesIO()
            chunk: bytes
            while True:
                chunk = con.recv(CLIENT_BUFFER)
                if chunk.endswith(b'\x17') or not chunk:
                    data.write(chunk[0:-1])
                    break
                else:
                    data.write(chunk)

            logging.info(f'{client} Message received (TCP): {data.getvalue()}')

            bovine = handshake_pb2.Bovine()
            print(bovine)

            cache.close()
            with Cache(cache.directory) as reference:
                if data.getvalue():
                    reference.set('cache', data.getvalue())

        except socket.error as e:
            logging.error(f'Socket error: {e}')
        except Exception as e:
            logging.error(f'Other Socket error: {e}')
        finally:
            con.close()
            logging.info(f'{client} Negotiation process stopped')

        con.close()
        logging.info(f'{client} Conexão finalizada')
        
    def server(socket_):
        while (not stop_event.is_set()):
            try:
                conn = socket_.accept()
                x = threading.Thread(target=tcp_connection, args=conn)
                x.start()
            except (Exception,):
                continue

    tcp_socket.bind(('', 0))
    tcp_socket.listen()
    server_thread = threading.Thread(target=server, args=(tcp_socket,))
    server_thread.start()
    logging.info(' TCP server started')
    
    thread_list.append(server_thread)
    return tcp.getsockname()[1]

def ping():

    while (not stop_event.is_set()):
        if not cache.get('cache'):
            time.sleep(2)
            continue
                
        try:
            with urllib.request.urlopen('http://127.0.0.1:3000/ping') as f:
                print(f.getcode())

                req = urllib.request.Request('http://127.0.0.1:3000/')
                req.add_header('Content-Type', 'application/json')

                bovine = handshake_pb2.Bovine()
                bovine.ParseFromString(cache.get('cache'))
                data = {
                    'category': bovine.category,
                    'sex': bovine.sex,
                    'weight': bovine.weight,
                    'earring': {
                        'value': bovine.earring.value,
                        'color': bovine.earring.color,
                    }
                }
                response = urllib.request.urlopen(
                    req, json.dumps(data).encode())

                print(response)
                
                del cache['cache']
        except (Exception,):
            pass

        time.sleep(2)

thread_list = []
tcp = setup_tcp_socket()
udp = setup_udp_socket()

def stop_sockets(tcp, udp):
    def _handler(signum, frame):
        print('')
        stop_event.set()
        send_broadcast.set()
        
        try:
            tcp.shutdown(socket.SHUT_RDWR)
        except (Exception,):
            pass
        
        tcp.close()
        logging.info(' Monitoring of TCP messages stopped')
        
        try:
            udp.shutdown(socket.SHUT_RDWR)
        except (Exception,):
            pass
        
        udp.close()
        logging.info(' Monitoring of UDP messages stopped')
        
        sys.exit(0)
        
    return _handler

tcp_port = tcp_server(tcp)
udp_service(udp, tcp_port)

ping_thread = threading.Thread(target=ping)
ping_thread.start()

signal.signal(signal.SIGINT, stop_sockets(tcp, udp))

send_broadcast.set()

while True:
    mode = input('Enter your input:')
    print(mode)
    if mode == ' ':
        send_broadcast.set()
    