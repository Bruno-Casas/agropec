from copy import deepcopy
import Collection

import protobuf.negotiation_pb2 as negotiation_pb2
from protobuf.ProtoMessage import ProtoMessage
from .Package import Package


CollectionDto = negotiation_pb2.Collection

class CollectionChain(Collection, ProtoMessage):
    first = None
    head = None
    
    def __init__(self, setup=None):
        if type(setup) == CollectionDto:
            self.load_from_dto(setup)
        elif type(setup) == Package:
            self.head = setup
        elif setup is not None:
                self.head = Package(setup)
        
    def get_message(self):
        dto = CollectionDto()
        dto.sum = 'Deveria ser um hash'
        
        current = self.first
        pkgs_dtos = []
        while current:
            pkgs_dtos.append(current.get_dto())
            current = current.next
        
        dto.packages.extend(pkgs_dtos)
        
        return dto
    
    def load_from_dto(self, dto: CollectionDto):
        self.sum = dto.sum
        
        for pkg in dto.packages:
            self.append(Package(pkg))
        
    @property
    def last(self):
        curr = self.first
        if not curr:
            return curr
        
        while curr.next:
            curr = curr.next
            
        return curr
  
    def add_package(self, new_package: Package):
            if not self.first:
                self.first = new_package
                return
        
            last = self.last
            
            if last:
                new_package.prior = last
                last.next = new_package
                self.head = last
            else:
                self.head = new_package
                
            self.head = new_package
            
    def get_package(self, index):
        pkg = PackageDto()
        with open(f'{index}/data.bin', 'rb', opener=self._opener()) as f:
            pkg.ParseFromString(f.read())
            
        return pkg
            
    def append_collection(self, chain):
        clone = deepcopy(chain)
        new_package = clone.first
    
        self.append(new_package)
                
    def insert(self, new_element, position):
        count=0
        current = self.first
        if position == 0:
            new_element.next = current
            self.head.prior = new_element
            self.head = self.last
            self.first = new_element
            return
            
        while current:
            if count == position:
                new_element.prior = current.prior
                current.prior.next = new_element
                new_element.next = current
                current.prior = new_element
                
                return
            else:
                count += 1
                current = current.next
            # break

        pass
    
    def insert_collection(self, chain, position):
        clone = deepcopy(chain)
        firt = clone.first
        last = clone.last
    
        count=0
        current = self.first
        if position == 0:
            last.next = current
            self.head.prior = last
            self.head = self.last
            self.first = firt
            return
            
        while current:
            if count == position:
                last.prior = current.prior
                current.prior.next = firt
                last.next = current
                current.prior = last
                
                return
            else:
                count += 1
                current = current.next
            # break

        pass
    
    
    def print(self):
        current = self.first
        while current:
            print(current.data, current, current.__dict__)
            current = current.next
            