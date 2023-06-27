import hashlib
import json
from typing import Any

from sno.protobuf.ProtoMessage import ProtoMessage
from .ChainList import ChainList

import sno.protobuf.negotiation_pb2 as negotiation_pb2


PackageDto = negotiation_pb2.Package

class Package(ChainList, ProtoMessage):
    _locator = None
    
    def __init__(self, data: Any = None): 
        
        if type(data) == PackageDto:
            self.load_from_dto(data)
        elif data is not None:       
            self.data = json.dumps(data)
            self.sum = hashlib.sha1(self.data.encode()).hexdigest()
            
    def get_parsed_data(self):
        return json.loads(self.data)
       
    def get_message(self):
        dto = PackageDto()
        dto.data = self.data.encode()
        dto.sum = self.sum
        
        return dto
    
    def load_from_dto(self, dto):
        self.data = dto.data
        self.sum = dto.sum
    
    @property
    def locator(self):
        return self._locator
        
    @locator.setter
    def locator(self, locator: Any):
        if self._locator is not None:
            raise ValueError('Locator has seted')
        
        self._locator = locator

