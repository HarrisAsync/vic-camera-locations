import os
import psycopg2
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Implement singleton pattern for database connection."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialize_db_connection()
                cls._instance._initialize_models()
        return cls._instance

    def _initialize_db_connection(self):
        """Initialize database connection."""
        self.conn = psycopg2.connect(DATABASE_URL)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def _initialize_models(self):
        """Initialize models inside the database instance."""
        from data.suburbs import Suburb  # Import here to avoid circular import issues
        self.suburb = Suburb(self)
        from data.roads import Road
        self.road = Road(self)

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query with optional fetching."""
        self.cur.execute(query, params or ())
        if fetch_one:
            return self.cur.fetchone()
        if fetch_all:
            return self.cur.fetchall()

    def close_connection(self):
        """Close the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close_connection()
