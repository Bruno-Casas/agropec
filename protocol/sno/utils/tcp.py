

from io import BytesIO
from sno.constants import CLIENT_BUFFER

EXIT_BYTE = b'\x00'
END_OF_MESSAGE_BYTE = b'\x17'
END_OF_NEGOTIATION_BYTE = b'\x04'


def recive_data(connection) -> bytes:
    data = BytesIO()
    while True:
        chunk = connection.recv(CLIENT_BUFFER)
        
        if chunk == EXIT_BYTE:
            raise ConnectionRefusedError('Connection stoped by pair')
        
        if chunk.endswith(END_OF_MESSAGE_BYTE) or not chunk:
            data.write(chunk[0:-1])
            break
        else:
            data.write(chunk)

    return data.getvalue()

def send_data(connection, data: bytes):
    data += END_OF_MESSAGE_BYTE
    connection.sendall(data)
    
def send_exit(connection):
    connection.sendall(EXIT_BYTE)
