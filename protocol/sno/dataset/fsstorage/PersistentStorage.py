import os
import sqlite3
from typing import List, Union
from uuid import UUID
from ..CollectionList import CollectionList

from ..SingletonMeta import SingletonMeta

from .Tag import Tag

from ..Collection import Collection
from ..Package import Package
from ..Storage import Storage

from ..constans import DATA_PATH

class PersistentStorage(Storage, metaclass=SingletonMeta):
    
    def __init__(self, id: str = 'data'):   
        
        def get_by_locator(locator):
            if locator:
                return self.get_package(*locator)
            
            return None
            
        try:
            if not os.path.exists(DATA_PATH):
                os.mkdir(DATA_PATH)
        except (Exception,):
            pass
            
        self.conn = sqlite3.connect(os.path.join(DATA_PATH, id + '.db'), check_same_thread=False)
        self.setup_db()
        
        self._pkg_tag = Tag(
            get_by_locator,
            lambda pkg: pkg.locator
        )
        
        self._collection_tag = Tag(
            lambda uuid: self.get_collection(uuid),
            lambda collection: collection.uuid
        )
        
    def setup_db(self):
        cursor = self.conn.cursor()
        
        cursor.executescript("""
            BEGIN;
            
            PRAGMA foreign_keys = ON;
                             
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT NOT NULL PRIMARY KEY,
                int_value INTEGER,
                text_value TEXT,
                byte_value BLOB
            );   

            CREATE TABLE IF NOT EXISTS collection (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                uuid TEXT NOT NULL UNIQUE,
                closed BOOLEAN DEFAULT false,
                prior_id INTEGER,
                next_id INTEGER,
                FOREIGN KEY (prior_id) REFERENCES collection(id),
                FOREIGN KEY (next_id) REFERENCES collection(id)
            );
            CREATE INDEX IF NOT EXISTS index_collection_uuid ON collection(uuid);

            CREATE TABLE IF NOT EXISTS package (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                count INTEGER NOT NULL,
                collection_id INTEGER NOT NULL,
                sum TEXT NOT NULL,
                data BLOB NOT NULL,
                prior_id INTEGER,
                next_id INTEGER,
                FOREIGN KEY (collection_id) REFERENCES collection(id) ON DELETE CASCADE,
                FOREIGN KEY (prior_id) REFERENCES package(id),
                FOREIGN KEY (next_id) REFERENCES package(id)
            );
            
            COMMIT;
        """)
        
    def update_indexes(self, collection):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT pc.uuid, nc.uuid, c.closed
                FROM collection c
                    LEFT JOIN collection pc ON c.prior_id = pc.id
                    LEFT JOIN collection nc ON c.next_id = nc.id
                WHERE c.uuid=?
            """,
            (str(collection.uuid),)
        )
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            collection._prior = result[0]
            collection._next = result[1]
            collection.closed = result[2]
  

    def create_collection(self, uuid: Union[str, UUID, None] = None):
        collection = Collection(None, uuid)
        collection._storage = self
        collection.tag = self._collection_tag
            
        cursor = self.conn.cursor()
        collection_id = self._check_collection(uuid)
        if collection_id:
            cursor.execute(
                """
                    SELECT c.id, pc.uuid, nc.uuid, c.closed
                    FROM collection c
                        LEFT JOIN collection pc ON c.prior_id = pc.id
                        LEFT JOIN collection nc ON c.next_id = nc.id
                    WHERE c.uuid=?
                """,
                (uuid,)
            )
            result = cursor.fetchone()
            
            collection_id = result[0]
            
            if result:
                collection._prior = result[1]
                collection._next = result[2]
                collection.closed = result[3]
            
            return collection
        
        last_collection_metadata = self._get_last_collection_metadata()

        cursor.execute(
            'INSERT OR IGNORE INTO collection (uuid, prior_id) VALUES (?, ?)',
            (str(collection.uuid), last_collection_metadata[0])
            )
                
        if last_collection_metadata[0]:
            cursor.execute(
                'UPDATE collection SET next_id=?, closed=? WHERE id=?',
                (cursor.lastrowid, True, last_collection_metadata[0])
            )
            
            collection._prior = last_collection_metadata[1]
            
        cursor.execute('commit')
        cursor.close()
                
        return collection

    def get_collection(self, uuid: str):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT pc.uuid, nc.uuid, c.closed
                FROM collection c
                    LEFT JOIN collection pc ON c.prior_id = pc.id
                    LEFT JOIN collection nc ON c.next_id = nc.id
                WHERE c.uuid=?
            """,
            (uuid,)
        )
        result = cursor.fetchone()
        
        if result:
            collection = Collection(None, uuid)
            collection._storage = self
            collection.tag = self._collection_tag
            
            collection._prior = result[0]
            collection._next = result[1]
            collection.closed = result[2]

            return collection
        else:
            return None
    
    def append_package(self, pkg: Package, collection_uuid: str, atomic=True):
        collection_id = self._check_collection(collection_uuid)
        if not collection_id:
            raise ValueError('Não é possível localizar')
        
        if self._check_package(collection_id, pkg.sum):
            return
        
        metadata = self._get_last_package_metadata(collection_id)
        if metadata:
            prior_id = metadata[0] 
            index = metadata[1] + 1    
        else:
            prior_id = None
            index = 0
        
        cursor = self.conn.cursor()
        
        cursor.execute(
            'INSERT OR IGNORE INTO package (collection_id, count, sum, data, prior_id) VALUES (?, ?, ?, ?, ?)',
            (collection_id, index, pkg.sum, pkg.data, prior_id)
        ) 
        
        if prior_id:
            cursor.execute(
                'UPDATE package SET next_id=? WHERE id=?',
                (cursor.lastrowid, prior_id)
            )
        
        if atomic:
            cursor.execute('commit')
            
        cursor.close()
            
    def get_package(self, collection_uuid: int, position: int = None) -> Package:
        collection_id = self._check_collection(collection_uuid)
        if not collection_id:
            raise ValueError('Não é possível localizar')
        
        cursor = self.conn.cursor()
        cursor.execute(
            """
                SELECT p.count, p.sum, p.data, pp.count as ppcount, np.count as npcount
                FROM package p
                    LEFT JOIN package pp ON p.prior_id = pp.id
                    LEFT JOIN package np ON p.next_id = np.id
                WHERE p.collection_id=? and p.count=?
                ORDER BY p.count
            """,
            (collection_id, position)
        )
        result = cursor.fetchone()
        
        pkg = None
        if result:
            pkg = Package()
            pkg.sum = result[1]
            pkg.data = result[2]
            pkg.locator = (collection_uuid, result[0])
            
            if result[3]:
                pkg._prior = (collection_uuid, result[3])
            
            if result[4]:
                pkg._next = (collection_uuid, result[4])
                
            pkg.tag = self._pkg_tag
        
        return pkg
    
    def append_collections(self, collections: List[Collection]):
        cursor = self.conn.cursor()
        
        last_id, last_uuid = self._get_last_collection_metadata()
        
        first = False
        for collection in collections:
            collection_id = self._check_collection(collection.uuid)
            if collection_id:
                continue
            
            if last_id:
                collection._prior = last_uuid  

            cursor.execute(
                'INSERT INTO collection (uuid, prior_id) VALUES (?, ?)',
                (str(collection.uuid), last_id)
                )
                    
            if last_id:
                cursor.execute(
                    'UPDATE collection SET next_id=? WHERE id=?',
                    (cursor.lastrowid, last_id)
                )
                
                collection._prior = last_uuid
                
            last_id = cursor.lastrowid
            last_uuid = str(collection.uuid)
            
            for pkg in collection.iter_packages:
                self.append_package(pkg, str(collection.uuid), False)

                
        cursor.execute('commit')
        cursor.close()
    
    def insert_collections_init(self, collections: List[Collection]): 
        cursor = self.conn.cursor()
        
        first_id, _ = self._get_first_collection_metadata()
        
        last_id = None
        for i, collection in enumerate(collections):
            collection_id = self._check_collection(collection.uuid)
            if collection_id:
                continue

            cursor.execute(
                'INSERT INTO collection (uuid, prior_id) VALUES (?, ?)',
                (str(collection.uuid), last_id)
                )
                    
            if last_id:
                cursor.execute(
                    'UPDATE collection SET next_id=? WHERE id=?',
                    (cursor.lastrowid, last_id)
                )
                
                
            last_id = cursor.lastrowid
            
            for pkg in collection.iter_packages:
                self.append_package(pkg, str(collection.uuid), False)

        if last_id:
            cursor.execute(
                    'UPDATE collection SET next_id=? WHERE id=?',
                    (first_id, last_id)
                )
            
            if first_id:
                cursor.execute(
                        'UPDATE collection SET prior_id=? WHERE id=?',
                        (last_id, first_id)
                    )
                
        cursor.execute('commit')
        cursor.close()

            
    def _check_collection(self, collection_uuid: str) -> int:
        collection_id = None
        
        if collection_uuid:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT id FROM collection WHERE uuid=?", (str(collection_uuid),))
                result = cursor.fetchone()

                if result:
                    collection_id = result[0]
            finally:
                cursor.close()      
            
        return collection_id
    
    def _check_package(self, collection_id: int, sum: str) -> int:
        package_id = None
        
        if collection_id:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT id FROM package WHERE collection_id=? and sum=?", (str(collection_id), sum))
                result = cursor.fetchone()

                if result:
                    package_id = result[0]
            finally:
                cursor.close()      
            
        return package_id
    
    def _get_last_collection_metadata(self) -> int:
        collection_id = (None, None)

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, uuid FROM collection where next_id is NULL")
            result = cursor.fetchone()

            if result:
                collection_id = (result[0], result[1])
        finally:
            cursor.close()      
            
        return collection_id
    
    def _get_first_collection_metadata(self) -> int:
        collection_id = (None, None)

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, uuid FROM collection where prior_id is NULL")
            result = cursor.fetchone()

            if result:
                collection_id = (result[0], result[1])
        finally:
            cursor.close()      
            
        return collection_id 
    
    def _get_last_package_metadata(self, collection_id: int) -> Package:
        if collection_id:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT id, count FROM package WHERE collection_id=? ORDER BY count DESC", (collection_id,))
                return cursor.fetchone()
            finally:
                cursor.close()      
            
        pass
    
    def count_collections(self, include_open: bool = False):
        count = 0

        cursor = self.conn.cursor()
        try:
            if include_open:
                cursor.execute("SELECT COUNT(*) FROM collection")
            else:
                cursor.execute("SELECT COUNT(*) FROM collection where closed = true")
                
            result = cursor.fetchone()

            if result:
                count = result[0]
        finally:
            cursor.close()      
            
        return count

    def get_all_collections(self):
        _, fisrt_uuid = self._get_first_collection_metadata()
        
        return CollectionList(self.get_collection(fisrt_uuid))
    
    def delete_collection(self, collection_uuid: str):
        collection_id = self._check_collection(collection_uuid)
        if not collection_id:
            raise ValueError('Não é possível localizar')
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('UPDATE collection SET prior_id=NULL WHERE prior_id=?', (collection_id,))
            cursor.execute('UPDATE collection SET next_id=NULL WHERE next_id=?', (collection_id,))
            cursor.execute("DELETE FROM package WHERE collection_id=?", (collection_id,))
            cursor.execute("DELETE FROM collection WHERE id=?", (collection_id,))
            
            cursor.execute('commit')
        finally:
            cursor.close()
            
    def close_collection(self, collection_uuid: str):
        collection_id = self._check_collection(collection_uuid)
        if not collection_id:
            raise ValueError('Não é possível localizar')
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('UPDATE collection SET closed=true WHERE id=?', (collection_id,))
            
            cursor.execute('commit')
        finally:
            cursor.close()  
        
    