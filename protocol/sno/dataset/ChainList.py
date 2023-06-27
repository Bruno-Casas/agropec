import abc
from uuid import UUID
from typing import Any, TypeVar, Generic

T = TypeVar('T')

class ChainList(Generic[T]):
    __metaclass__ = abc.ABCMeta
    
    uuid: UUID
    _head = None
    _type = None
    _prior = None
    _next = None
    _tag = None
    
    def __new__(cls, *args, **kwargs):
        instance = super(ChainList, cls).__new__(cls)
        instance._type = cls
        return instance
    
    @property
    def prior(self):
        if self._tag:
            return self._tag.read_transform(self._prior)
        
        return self._prior

    @prior.setter
    def prior(self, value):
        if self._tag:
            self._prior = self._tag.write_transform(value)
            return
        
        if value is None or isinstance(value, self._type):
            self._prior = value
        
        raise ValueError('Invalid type for the prior')
        
    @property
    def next(self):
        if self._tag:
            return self._tag.read_transform(self._next)
        
        return self._next

    @next.setter
    def next(self, value):
        if self._tag:
            self._next = self._tag.write_transform(value)
            return
        
        if isinstance(value, self._type):
            self._next = value
        
        raise ValueError('Invalid type for the prior')
    
    @property
    def is_tagged(self):
        return self._tag is not None
    
    @next.setter
    def is_tagged(self):
        raise ValueError('Readonly value')
    
    @property
    def tag(self):
        return self._next
    
    @next.setter
    def tag(self, tag: Any):
        if self._tag is not None:
            raise ValueError('Elemenrts has old tag')
        
        self._tag = tag
    
    def __iter__(self):
        self._head = self
        return self
    
    def __next__(self):
        current = self._head
            
        if current:
            self._head = current.next
            return current
        
        raise StopIteration  # Done iterating.
