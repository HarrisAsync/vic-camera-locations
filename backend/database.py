import os
import psycopg2
import threading
from psycopg2.pool import ThreadedConnectionPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    _instance = None
    _lock = threading.Lock()
    _pool = None  # We'll store the connection pool here

    def __new__(cls):
        """Singleton pattern for the Database class."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialize_pool()
                cls._instance._initialize_models()
        return cls._instance

    def _initialize_pool(self):
        """
        Initialize a threaded connection pool.
        Adjust minconn / maxconn as needed for your workload.
        """
        self._pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=DATABASE_URL
        )

    def _initialize_models(self):
        """
        Import and initialize models here to avoid circular imports.
        You can keep the same structure as your existing code.
        """
        from data.suburbs import Suburb  # Import here to avoid circular import issues
        self.suburb = Suburb(self)

        from data.roads import Road
        self.road = Road(self)

        from data.cameras import Camera
        self.camera = Camera(self)

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """
        Execute a query with optional fetching, keeping the same interface.
        We borrow a connection from the pool, use it briefly, then return it.
        """
        conn = self._pool.getconn()
        try:
            # Optionally set autocommit on each borrowed connection, if needed
            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute(query, params or ())
                if fetch_one:
                    return cur.fetchone()
                if fetch_all:
                    return cur.fetchall()
                # If neither fetch_one nor fetch_all is True, we simply execute the query
        finally:
            # Always return the connection to the pool
            self._pool.putconn(conn)

    def close_pool(self):
        """Close the entire pool (all connections)."""
        if self._pool:
            self._pool.closeall()

    def __del__(self):
        """Ensure pool is closed when the instance is deleted."""
        self.close_pool()
