#!/usr/bin/env python

import time

from chafon_rfid.base import ReaderCommand, ReaderResponseFrame
from chafon_rfid.command import (CF_SET_BUZZER_ENABLED, CF_SET_RF_POWER)
from chafon_rfid.response import G2_TAG_INVENTORY_STATUS_MORE_FRAMES
from chafon_rfid.transport_serial import SerialTransport
from chafon_rfid.uhfreader288m import G2InventoryCommand, G2InventoryResponseFrame

import socket
import threading

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
DELAY = 0.05

def read_tag():
    
    def run_command(transport, command):
        transport.write(command.serialize())
        return ReaderResponseFrame(transport.read_frame()).result_status
    
    transport = SerialTransport(device='/dev/ttyUSB0')
    get_inventory_cmd = G2InventoryCommand(q_value=4, antenna=0x80)
    frame_type = G2InventoryResponseFrame
    run_command(transport, ReaderCommand(CF_SET_RF_POWER, data=[26]))
    run_command(transport, ReaderCommand(CF_SET_BUZZER_ENABLED, data=[True]))

    tag = None
    while not tag:
        transport.write(get_inventory_cmd.serialize())
        inventory_status = None
        while inventory_status in [G2_TAG_INVENTORY_STATUS_MORE_FRAMES, None]:
            resp = frame_type(transport.read_frame())
            inventory_status = resp.result_status
            tag = next(resp.get_tag(), None)
            
        time.sleep(DELAY)
     
    transport.close()   
    return tag

def connection(con, client):
    print(client, 'Nova conexão')
    
    tag = read_tag()
    con.send(tag.epc.hex().encode() + b'\x04') 
    print(client, 'Tag enviada: EPC %s, RSSI %s' % (tag.epc.hex(), tag.rssi)) 
    
    con.close()
    print(client, 'Conexão finalizada')
    print('------')

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen()

while True:
    con, client = tcp.accept()
    x = threading.Thread(target=connection, args=(con, client))
    x.start()
    x.join()
