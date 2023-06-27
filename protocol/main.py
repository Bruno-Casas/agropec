# from dataset import FsCollection
# from dataset.api import count_collection, get_collection_list
# from dataset.Package import Package, PackageDto
# from dataset.constans import DATA_PATH
from sno.dataset.Collection import Collection
from sno.dataset.Package import Package
from sno.dataset.ChainList import ChainList
from sno.dataset.fsstorage.PersistentStorage import PersistentStorage

# storage = PersistentStorage()

# c = storage.create_collection()
# c.append_package(Package('Isso é uma teste1'))
# c.append_package(Package('Isso é uma teste2'))

# storage2 = PersistentStorage('data2')
# c2 = storage2.create_collection()
# c2.append_package(Package('Isso é uma teste3'))
# c2.append_package(Package('Isso é uma teste4'))

# c3 = storage2.create_collection()
# c3.append_package(Package('Isso é uma teste5'))
# c3.append_package(Package('Isso é uma teste6'))

# c.insert_collections_init([c2])

# pkg = c.get_package(1)
# pp = pkg.prior
# np = pkg.next

# print(pp.get_message())
# print(pkg.get_message())
# print(np.get_message())

# cdto = c.get_message()
# print(cdto)

# print('\n\nTEste\n\n')

# c2 = Collection(storage, dto=cdto)
# pkg = c2.get_package(1)
# pp = pkg.prior
# np = pkg.next
# print(pp.get_message())
# print(pkg.get_message())
# print(np.get_message())

# print(c.prior.get_message())

# pass


from sno.Conveyor import Conveyor
import sys

from sno.constants import DB_NAME

from sno.base_modules.PingModule import PingModule

# storage = PersistentStorage(id=DB_NAME)

# c = storage.create_collection()
# c.append_package(Package('Isso é uma teste1'))
# c.append_package(Package('Isso é uma teste2'))

# storage = PersistentStorage()

# c = storage.create_collection()
# c.append_package(Package('Isso é uma teste7'))
# c.append_package(Package('Isso é uma teste8'))

# storage = PersistentStorage()

# c = storage.create_collection()
# c.append_package(Package('Isso é uma teste3'))
# c.append_package(Package('Isso é uma teste4'))

service = Conveyor()
service.load_module(PingModule)
service.start()

while True:
    try:
        mode = input('')
    except KeyboardInterrupt:
        service.stop()
        sys.exit(0)
     
    if mode == 'u':
        service.dispatch_event('broadcast')

pass


# UdpClient()
# UdpClient2()





# import asyncio
# import random
# from threading import Thread
# import time

# queue = None

# async def worker(name):
#     #while True:
#         # # Get a "work item" out of the queue.
#         # sleep_for = await queue.get()

#         # # Sleep for the "sleep_for" seconds.
#         # await asyncio.sleep(sleep_for)

#         # # Notify the queue that the "work item" has been processed.
#         # queue.task_done()

#     print('\r' + name, end='')
        
# async def workerc(name, queue):
#     while True:
#         # mode = input('Char: ')
#         # print(mode)
#         await asyncio.sleep(1)
#         queue.put_nowait("mode")
#         # if mode == 'u':
#         #     queue.put_nowait(mode)


# async def main():
#     # Create a queue that we will use to store our "workload".
#     global queue
#     queue = asyncio.Queue()

#     taskc = asyncio.create_task(workerc(f'worker-', queue))
#     while True:
#         teste = await queue.get()
        
#         task = asyncio.create_task(worker(teste))


#     print('====')
#     print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
#     print(f'total expected sleep time: {total_sleep_time:.2f} seconds')




# def aserver():
#     asyncio.run(main())
    
    
    
# thread = Thread(target=aserver)
# thread.start()
    
# while True:
#     mode = input('A:')
#     if mode == 'u':
#         queue.put_nowait("mode2")


