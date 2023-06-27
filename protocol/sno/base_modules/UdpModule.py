
from io import BytesIO
import logging
import socket
import threading
from time import sleep

from sno.constants import DB_NAME
from ..dataset.fsstorage.PersistentStorage import PersistentStorage
from sno.utils.tcp import recive_data, send_data
from sno.base_modules.EventModule import event
from sno.base_modules.AsyncModule import AsyncModule
from ..dataset.CollectionList import CollectionList
from sno.constants import CLIENT_BUFFER
import sno.protobuf.udp_pb2 as udp_pb2
import sno.protobuf.tcp_pb2 as tcp_pb2
import sno.protobuf.handshake_pb2 as handshake_pb2
import sno.protobuf.negotiation_pb2 as negotiation_pb2

logging.basicConfig(level=logging.DEBUG)

storage = PersistentStorage(id=DB_NAME)

class UdpModule(AsyncModule):
    _tcp_port = 0
    
    def setup(self, tcp_state):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self._tcp_registry = tcp_state.get('registry')
        
    @event('broadcast')
    def broadcast(self):
        udp_hello = udp_pb2.UdpHello()
        udp_hello.port = self._tcp_port

        for port in range(37020, 37023):
            logging.info(' Sending UDP broadcast message to port ' + str(port))
            self._socket.sendto(udp_hello.SerializeToString(), ('<broadcast>', port))

    def run(self):
        port = 37020
        while True:
            try:
                self._socket.bind(('', port))
                break
            except (Exception,):
                port += 1
                pass
        
        sleep(1)    
        self._tcp_port = self._tcp_registry.get('tcp_port')
        
        logging.info(' UDP server started in port ' + str(port))
        while (not self.stop_event.is_set()):
            resp = self._socket.recvfrom(1024)
            if resp[1] and (resp[1][1] != port or resp[1][0] != self.host_ip):
                x = threading.Thread(target=_udp_connection, args=resp)
                x.start()
                
    def stop(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except (Exception,):
            pass
        
        self._socket.close()
        logging.info(' Monitoring of UDP messages stopped')
    
def _udp_connection(data, addr):
    udp_hello = udp_pb2.UdpHello()
    udp_hello.ParseFromString(data)
    print(udp_hello.port)

    logging.info(f'{addr} Message received (broadcast): {udp_hello.port}')
    logging.info(f'{addr} Starting negotiation process')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((addr[0], udp_hello.port))

    try:
        hand_shake = tcp_pb2.HandShake()
        hand_shake.hash = 'testehash'
        
        send_data(sock, hand_shake.SerializeToString())
        
        server_summary = negotiation_pb2.DataSummary()
        server_summary.ParseFromString(recive_data(sock))
        print('S: ', server_summary.chain_size)
        
        local_count = storage.count_collections()
        summary = negotiation_pb2.DataSummary()
        summary.chain_size = local_count
        send_data(sock, summary.SerializeToString())
        
        cl = negotiation_pb2.CollectionList()
        cl.ParseFromString(recive_data(sock))
        
        dto = storage.get_all_collections().get_message()
        send_data(sock, dto.SerializeToString())
        
        remote_count = server_summary.chain_size
        if not remote_count or local_count == remote_count:
            return
        
        colls = CollectionList(cl)
        if local_count > remote_count:
            storage.append_collections(colls)
        else:
            storage.insert_collections_init(colls)
        
    except socket.error as e:
        logging.error(f'Socket error: {e}')
    except Exception as e:
        logging.error(f'Other Socket error: {e}')
    finally:
        sock.close()
        logging.info(f'{addr} Negotiation process stopped')            
