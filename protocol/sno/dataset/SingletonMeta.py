class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not (cls in cls._instances and kwargs.get('id') in cls._instances.get(cls, {})):
            cls._instances[cls] = {kwargs.get('id'): super().__call__(*args, **kwargs)}
            
        return cls._instances[cls][kwargs.get('id')]
