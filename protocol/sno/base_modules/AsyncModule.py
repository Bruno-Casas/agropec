
from threading import Event

from .EventModule import EventModule


class AsyncModule(EventModule):
    
    _stop_event: Event = None
    
    def __new__(cls):
        instance = super(AsyncModule, cls).__new__(cls)
        instance.stop_event = Event() 
        return instance
    
    def run(self):
        """run function"""
        pass
    
    def stop(self):
        self.stop_event.set()
