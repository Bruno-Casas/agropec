from multiprocessing import Event
from threading import Thread
from time import sleep
from typing import Dict, Type
from .base_modules.CoreEventModule import CoreEventModule
from .base_modules.AsyncModule import AsyncModule
from .base_modules.EventModule import EventModule
from .base_modules.Module import Module


class ModularService():
    _modules_record = {}
    registers = {}
    
    _event_module = CoreEventModule()
    
    def __new__(cls):
        instance = super(ModularService, cls).__new__(cls)
        
        instance._event_record = instance._event_module._event_record
        instance._process_module(instance._event_module)
        
        return instance
    
    def load_module(self, module_class: Type[Module], setup_args: tuple = ()):
        module = module_class()
        return self._process_module(module, setup_args)
        
    def _process_module(self, module: Module, setup_args: tuple = ()):
        module.setup(*setup_args)
        module.set_context(self)
        
        if isinstance(module, EventModule):
            self._event_record.update(module._event_record)
            self._modules_record[module.id] = (None, module)
        
        if isinstance(module, AsyncModule):
            thread = Thread(target=module.run)
            self._modules_record[module.id] = (thread, module)
            
        return module.state
        
    def start(self):
        for module in self._modules_record.values():
            if module[0]:
                module[0].start()

    def stop(self):
        for module in self._modules_record.values():
            module[1].stop_event.set()
            module[1].stop()
            
    def join(self):
        for module in self._modules_record.values():
            module[0].join()       

    def dispatch_event(self, name: str):
        self._event_module.call_event(name)
