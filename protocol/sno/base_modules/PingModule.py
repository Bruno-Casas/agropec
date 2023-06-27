import json
import time

import urllib.request
from sno.base_modules.AsyncModule import AsyncModule
from sno.dataset.fsstorage.PersistentStorage import PersistentStorage

from sno.dataset import Collection

from sno.constants import DB_NAME

class PingModule(AsyncModule):
    _storage = PersistentStorage(id=DB_NAME)
    
    def run(self):
        while (not self.stop_event.is_set()):
            try:
                time.sleep(2)
                
                count = self._storage.count_collections()
                if not count:
                    continue

                urllib.request.urlopen('http://127.0.0.1:3000/api/rest/ping')
            except Exception as e:
                continue
                
            try:
                collections = list(iter(self._storage.get_all_collections()[0]))  

                req_data = []
                collection: Collection
                for collection in collections:
                    if collection.closed and collection.packages:
                        req_data.append({
                            'uuid': str(collection.uuid),
                            'packages': [pkg.get_parsed_data() for pkg in collection.packages]
                        }) 
                        
                pass
                if not req_data:
                    continue

                print('Sending ' + str(len(req_data)) + ' collections to master')
                req = urllib.request.Request('http://127.0.0.1:3000/api/rest/bovine')
                req.add_header('Content-Type', 'application/json')
                
                response = urllib.request.urlopen(req, json.dumps(req_data).encode())
                
                for collection in collections:
                    if collection.closed:
                        self._storage.delete_collection(str(collection.uuid))

                print(response)
            except Exception as e:
                print('Error in send data:' + str(e))
            
        pass
