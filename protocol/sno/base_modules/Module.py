

from multiprocessing import Event


class Module():  
    state = {} 
    
    def __new__(cls):
        instance = super(Module, cls).__new__(cls)
        instance.id = id(cls)
        instance.state = {
            'started': Event(),
            'registry': {}
        }
    
        return instance
    
    def setup(self):
        """setup function"""
        pass
    
    def set_context(self, context):
        self.context = context
