import random
import signal
import socket
import string
import sys
import threading

import webview
from sno.Conveyor import Conveyor

from sno.dataset.fsstorage.PersistentStorage import PersistentStorage

from sno.dataset.Package import Package
from sno.base_modules.PingModule import PingModule

from sno.dataset.constans import DATA_PATH

service = Conveyor()
service.load_module(PingModule)
service.start()

def client(host='localhost', port=5000): 
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #sock.connect((host, port))

    try: 
        # data = BytesIO()
        # chunk: bytes
        # while True:
        #     chunk = sock.recv(CLIENT_BUFFER)
        #     if chunk.endswith(b'\x04') or not chunk:
        #         data.write(chunk[0:-1])
        #         break
        #     else:
        #         data.write(chunk)
                
        # print(data.getvalue().decode())
        return ''.join(random.choice(string.ascii_letters) for i in range(32))
    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        #sock.close() 
        pass

class Api:
    _storage = PersistentStorage()
    
    def __init__(self):
        self.collection = self._storage.create_collection()
        
    def close_collection(self):
        self.collection.close()
        
    def get_value(self):
        return {
            'message': client()
        }
        
    def store(self, data: str):
        print(data)
        pkg = Package(data)
        self.collection.append_package(pkg)
        
    def dispatch(self):
        service.dispatch_event('broadcast')


api = Api()
window = webview.create_window('Hello world', 'http://127.0.0.1:5173/', js_api=api)
def evaluate_js(window):
    result = window.evaluate_js(
            r"""
            document.addEventListener('keydown', (event) => {
                if (event.key == 'u') {
                    console.log('Dispatch event');
                    let api = window['pywebview'].api
                    api.dispatch()
                }
            }, false);
            """
        )

def on_closed():
    service.stop()
    window.destroy()
    api.close_collection()
    sys.exit(0)

window.events.closed += on_closed
webview.start(evaluate_js, window)