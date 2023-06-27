import inspect
from queue import Queue
from threading import Thread

from sno.base_modules.Module import Module


def event(name: str):
    def decorator(fn):
        
        def func(*args, **kwargs):
            Thread(target=fn, args=(*args, *(kwargs.values()))).start()
        
        func.event_name = name
         
        return func
    return decorator
    

class EventModule(Module):   
    
    _event_record = None
    _queue = None
    
    def __new__(cls):
        instance = super(EventModule, cls).__new__(cls)
        instance._event_record = {}
         
        for method in inspect.getmembers(instance, predicate=inspect.ismethod):
            fn = method[1]
            
            event_name = getattr(fn, 'event_name', None)
            if event_name:
                instance._event_record[event_name] = (Queue(), fn)
    
        return instance
    