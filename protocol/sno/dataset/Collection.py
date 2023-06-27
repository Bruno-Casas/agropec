import abc
from typing import List, Union
from uuid import UUID, uuid1
from .Storage import Storage

from sno.protobuf.ProtoMessage import ProtoMessage
from .ChainList import ChainList

import sno.protobuf.negotiation_pb2 as negotiation_pb2
from .Package import Package


CollectionDto = negotiation_pb2.Collection

class Collection(ChainList, ProtoMessage):
    uuid: UUID
    closed: bool
    size = 0
    first = None
    
    _storage:Storage = None
    
    def __new__(cls, storage: Storage, uuid: str = None, dto: CollectionDto = None):
        if type(dto) == CollectionDto:
            uuid = dto.uuid
        
        if storage:
            instance = storage.create_collection(uuid)
            instance._storage = storage
        else:   
            instance = super(Collection, cls).__new__(cls)
        
        instance.uuid = generate_uuid(uuid)
        
        instance._memory_pkgs = []
        
        return instance

    @property
    def packages(self):
        if self._storage:
            return list(self.iter_packages)
        else:
            return self._memory_pkgs
    
    @property
    def iter_packages(self):
        first = self.get_package(0)
        if first:
            return iter(first)
        
        return iter(())
    
    def append_package(self, pkg: Package):
        if self._storage:
            return self._storage.append_package(pkg, self.uuid)
        else:
            return self._memory_pkgs.append(pkg)

    def get_package(self, position: int) -> Package:
        if self._storage:
            return self._storage.get_package(self.uuid, position)
        else:
            return self._memory_pkgs[position]

    def append_collection(self, collection: 'Collection'):
        self.append_collections([collection])
    
    def insert_collection_init(self, collection: 'Collection'):
        self.insert_collections_init([collection])
    
    @abc.abstractmethod
    def append_collections(self, collections: List['Collection']):
        self._storage.append_collections(collections)
        self._storage.update_indexes(self)
    
    @abc.abstractmethod
    def insert_collections_init(self, collections: List['Collection']):
        self._storage.insert_collections_init(collections)
        self._storage.update_indexes(self)
    
    def close(self):
        self._storage.close_collection(self.uuid)
        
    def get_message(self):
        dto = CollectionDto()
        dto.uuid = str(self.uuid)
        
        current = self.get_package(0)
        pkgs_dtos = []
        while current:
            pkgs_dtos.append(current.get_message())
            current = current.next
        
        dto.packages.extend(pkgs_dtos)
        
        return dto
    
    def load_from_dto(self, dto: CollectionDto):
        self.uuid = UUID(dto.uuid)
        
        size = len(dto.packages)
        last = None
        for index, pkg_dto in enumerate(dto.packages):
            pkg = Package(pkg_dto)
            pkg.locator = (self.uuid, index)
            
            if last:
                pkg._prior = last
                
            if last and index < size:
                last._next = pkg
                
            self.append_package(pkg)
            
            last = pkg

def generate_uuid(uuid: Union[str, UUID, None] = None):
    type_ = type(uuid)
    
    if type_ is UUID:
        return uuid
    elif type_ is str:
        try:
            return UUID(uuid)
        except ValueError:
            raise ValueError('Invalid UUID format')
    elif uuid is None:
        return uuid1()
        
    raise ValueError('Invalid type for uuid parameter')