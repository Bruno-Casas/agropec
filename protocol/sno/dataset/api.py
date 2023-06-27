
# import os
# from dataset.Package import Package

# from .constans import DATA_PATH

# def del_collection(self, uuid):
#     os.remove(uuid, dir_fd=self.dir_fd)
    
# def list_collections_uuid():
#     list = os.listdir(DATA_PATH)

#     flist = []
#     for dir in list:
#         if os.listdir(os.path.join(DATA_PATH, dir)):
#             flist.append(dir)
            
#     return flist

# def list_collections():
#     collections_uuids = os.listdir(DATA_PATH)
    
#     collections = []
#     for uuid in collections_uuids:
        
#         with FsCollection(uuid) as fs_col:
#             col = Collection()
#             for pkg in fs_col.list_packages():
#                 col.append(Package(pkg))
            
#             collections.append(col)
        
#     return collections
 
# def get_collection_list():
#     list = CollectionList()
#     list.extend(list_collections())
    
#     return list

# def has_collection(uuid):
#     return os.path.exists(os.path.join(DATA_PATH, uuid))

# def count_collection():
#     _, dirs, _ = next(os.walk(DATA_PATH))
    
#     count = 0
#     for dir in dirs:
#         if os.listdir(os.path.join(DATA_PATH, dir)):
#             count += 1
            
#     return count
