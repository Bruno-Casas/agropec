
import abc

class ProtoMessage:
   __metaclass__ = abc.ABCMeta
   
   @abc.abstractmethod
   def get_message(self):
      pass
   
   @abc.abstractmethod
   def load_from_dto(self):
      pass
