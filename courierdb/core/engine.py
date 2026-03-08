import os
from typing import Dict, Generic, List, Optional, Type, TypeVar

import lmdb
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class CourierDBError(Exception):
    """Base exception for CourierDB"""
    pass


class Collection(Generic[T]):
    """
    Manages a single 'table' of data.
    Stores and retrieves JSON objects in LMDB.
    """

    def __init__(self, name: str, model_cls: Type[T], env: lmdb.Environment):
        self.name = name
        self.model_cls = model_cls
        self.env = env

        # Open collection DB
        self.main_db = self.env.open_db(f"{name}:main".encode(), create=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Don't close env here, CourierDB manages it

    def upsert(self, key: str, record: T):
        """
        Writes data.
        """
        json_data = record.model_dump_json()

        # Write Transaction (LMDB)
        with self.env.begin(write=True) as txn:
            txn.put(key.encode(), json_data.encode(), db=self.main_db)

    def read(self, key: str) -> Optional[T]:
        """Retrieves a record by primary key."""
        with self.env.begin(db=self.main_db, write=False) as txn:
            data = txn.get(key.encode())
            if not data:
                return None
            return self.model_cls.model_validate_json(data)

    def list(self, limit: int = 100, skip: int = 0) -> List[T]:
        """Scans records with pagination."""
        results = []
        with self.env.begin(db=self.main_db, write=False) as txn:
            cursor = txn.cursor()
            if not cursor.first():
                return []

            skipped = 0
            while skipped < skip:
                if not cursor.next():
                    return []
                skipped += 1

            count = 0
            for _, value in cursor.iternext(keys=True, values=True):
                if count >= limit:
                    break
                obj = self.model_cls.model_validate_json(value)
                results.append(obj)
                count += 1

        return results

    def delete(self, key: str) -> bool:
        """
        Deletes a record.
        """
        with self.env.begin(write=True) as txn:
            return txn.delete(key.encode(), db=self.main_db)

    def close(self):
        """Closes connections cleanly."""
        pass


class CourierDB:
    """Main entry point."""

    def __init__(self, storage_path: str = "./flow_data"):
        self.storage_path = storage_path
        self.collections: Dict[str, Collection] = {}

        # Ensure directories exist
        os.makedirs(storage_path, exist_ok=True)

        # Setup Shared LMDB Environment
        self.env = lmdb.open(
            os.path.join(storage_path, "data.lmdb"),
            max_dbs=100,  # Increased max_dbs for many collections
            map_size=10 * 1024 * 1024 * 1024,
        )
        self.registry_db = self.env.open_db(b"__courierdb__:collections", create=True)

    def _register_collection(self, name: str):
        with self.env.begin(write=True) as txn:
            txn.put(name.encode(), b"1", db=self.registry_db)

    def collection(self, name: str, model: Type[T]) -> Collection[T]:
        if name not in self.collections:
            self.collections[name] = Collection(name, model, self.env)
            self._register_collection(name)
        return self.collections[name]

    def list_collections(self) -> List[str]:
        """
        Lists all known collection names from the persistent registry.
        Returns a list of names like ['users', 'orders'].
        """
        collections: List[str] = []
        with self.env.begin(db=self.registry_db, write=False) as txn:
            cursor = txn.cursor()
            for key_bytes, _ in cursor:
                collections.append(key_bytes.decode())
        return sorted(collections)

    def close(self):
        """
        Closes all open collections and the underlying LMDB environment.
        """
        for name, col in self.collections.items():
            try:
                col.close()
                print(f"Closed collection: {name}")
            except Exception as e:
                print(f"Error closing collection {name}: {e}")
        self.collections.clear()
        self.env.close()
