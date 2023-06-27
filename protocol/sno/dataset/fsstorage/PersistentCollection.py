import os
import pickle
import uuid
from Collection import Collection

import CollectionChain

from ..Package import Package, PackageDto
from ..constans import DATA_PATH


class PersistentCollection(Collection):
        
    def append_package(self, index):
        pkg = PackageDto()
        with open(f'{index}/data.bin', 'rb', opener=self._opener()) as f:
            pkg.ParseFromString(f.read())
            
        return pkg
        
    def list_packages(self):
        packages = []
        for i in range(0, self.index):
            packages.append(self.get_package(i))
            
        return packages
    