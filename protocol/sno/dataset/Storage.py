import abc
from typing import List, Union
from uuid import UUID, uuid1

import sno.protobuf.negotiation_pb2 as negotiation_pb2
from .Package import Package


CollectionDto = negotiation_pb2.Collection

class Storage:
    __metaclass__ = abc.ABCMeta
    
    def open_collection(self, uuid: Union[str, UUID, None]):
        pass
  
    @abc.abstractmethod
    def get_collection(self, collection_id: int):
        pass
    
    @abc.abstractmethod        
    def append_package(self, pkg: Package, collection_uuid: str, index: int, atomic: bool):
        pass
    
    @abc.abstractmethod
    def get_package(self, collection_uuid: str, position: int) -> Package:
        pass
    
    @abc.abstractmethod
    def append_collections(self, collections: List):
        pass
    
    @abc.abstractmethod
    def insert_collections_init(self, collections: List):
        pass
    
    @abc.abstractmethod
    def update_indexes(self, collection):
        pass
    
    @abc.abstractmethod
    def count_collections(self):
        pass
    
    @abc.abstractmethod
    def get_collection_list(self):
        pass
    
    @abc.abstractmethod
    def delete_collection(self, collection_uuid: str):
        pass
    
    @abc.abstractmethod
    def close_collection(self):
        pass
    