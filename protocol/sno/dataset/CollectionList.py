from .fsstorage.Tag import Tag
from sno.protobuf.ProtoMessage import ProtoMessage
from .Collection import Collection
import sno.protobuf.negotiation_pb2 as negotiation_pb2

CollectionListDto = negotiation_pb2.CollectionList

class CollectionList(list, ProtoMessage):
    head = None
    _indexes = None
    
    def __init__(self, setup=None):
        super().__init__()
        
        self._indexes = {}
        collection_tag = Tag(
            lambda uuid: self._indexes[self.get(uuid)],
            lambda collection: collection.uuid
        )
        
        if type(setup) == CollectionListDto:
            
            for collection_dto in setup.collections:
                collection = Collection(None)
                collection.load_from_dto(collection_dto)
                collection.tag = collection_tag
                
                self.append(collection)
                self._indexes[collection.uuid] = len(self) -1

        elif type(setup) == Collection:
            self.append(setup)
        elif setup is None:
            pass
        else:
            raise ValueError('Invalid value in setup arg')

    def get_message(self):
        dto = CollectionListDto()
        
        current = self[0] if len(self) else None
        
        collections_tdo = []     
        while current:
            collections_tdo.append(current.get_message())
            current = current.next
        
        dto.collections.extend(collections_tdo)
        
        return dto
