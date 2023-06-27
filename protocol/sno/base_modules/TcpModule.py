import logging
import socket
import threading

from sno.constants import DB_NAME
from ..dataset.CollectionList import CollectionList
from ..dataset.fsstorage.PersistentStorage import PersistentStorage

from sno.utils.tcp import EXIT_BYTE, recive_data, send_data, send_exit
from sno.constants import CLIENT_BUFFER
from sno.base_modules.EventModule import event
from sno.base_modules.AsyncModule import AsyncModule
import sno.protobuf.tcp_pb2 as tcp_pb2
import sno.protobuf.handshake_pb2 as handshake_pb2
import sno.protobuf.negotiation_pb2 as negotiation_pb2

storage = PersistentStorage(id=DB_NAME)

class TcpModule(AsyncModule):
    
    _AUTH_HASH = 'testehash'
    
    def setup(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    @event('gbfvtb')
    def broadcast(self):
        hand_shake = handshake_pb2.HandShake()
        hand_shake.port = 9999 # tcp_server_port

        for port in range(37020, 37023):
            logging.info(' Sending UDP broadcast message to port ' + str(port))
            self._socket.sendto(hand_shake.SerializeToString(), ('<broadcast>', port))

    def run(self):
        self._socket.bind(('', 0))
        self._socket.listen()
        port = self._socket.getsockname()[1]
        self.state['registry']['tcp_port'] = port
        
        logging.info(f' TCP server started in port {port}')
        while (not self.stop_event.is_set()):
            try:
                conn = self._socket.accept()
                x = threading.Thread(target=tcp_connection, args=(*conn, self._AUTH_HASH))
                x.start()
            except (Exception,):
                continue                
    
    def stop(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except (Exception,):
            pass
        
        self._socket.close()
        logging.info(' Monitoring of TCP messages stopped')
    
    
def tcp_connection(con, client, auth_hash):
    logging.info(f'{client} New connection')

    #con.sendall((cache.get('cache') or b'') + b'\x17')
    #con.sendall(b'testehjd\x17')

    try:
        hand_shake = tcp_pb2.HandShake()
        hand_shake.ParseFromString(recive_data(con))
        
        if hand_shake.hash != auth_hash:
            send_exit(con)
            return
        
        local_count = storage.count_collections()
        
        summary = negotiation_pb2.DataSummary()
        summary.chain_size =  local_count# Tamanho 
        send_data(con, summary.SerializeToString())
        
        client_summary = negotiation_pb2.DataSummary()
        data = recive_data(con)
        client_summary.ParseFromString(data)
        
        dto = storage.get_all_collections().get_message()
        send_data(con, dto.SerializeToString())
        
        cl = negotiation_pb2.CollectionList()
        cl.ParseFromString(recive_data(con))
        
        remote_count = client_summary.chain_size
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
        con.close()
        logging.info(f'{client} Negotiation process stopped')
