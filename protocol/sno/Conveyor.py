
from sno.base_modules.TcpModule import TcpModule
from sno.base_modules.UdpModule import UdpModule
from sno.ModularService import ModularService


class Conveyor(ModularService):
    
    def __init__(self):
        tcp_state = self.load_module(TcpModule)
        self.load_module(UdpModule, (tcp_state,))
        
