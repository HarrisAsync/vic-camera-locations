from typing import List, Dict

class Suburb:
    def __init__(self, db):
        self.db = db  # Store the database instance

    def get_by_name(self, name: str) -> Dict:
        """Fetch a suburb by name."""
        query = "SELECT name, minlong, minlat, maxlong, maxlat FROM suburbs WHERE name = %s"
        row = self.db.execute_query(query, (name,), fetch_one=True)
        if row:
            return {
                "name": row[0],
                "minlong": row[1],
                "minlat": row[2],
                "maxlong": row[3],
                "maxlat": row[4],
            }
        return None
    
    def get_by_names(self, names: List[str]) -> List[Dict]:
        """Fetch multiple suburbs by a list of names."""
        if not names:
            return []
        
        placeholders = ', '.join([f"'{n}'" for n in names])  # Generate placeholders for SQL query
        query = f"""
            SELECT name, minlong, minlat, maxlong, maxlat 
            FROM suburbs 
            WHERE name IN ({placeholders})
        """
        rows = self.db.execute_query(query, tuple(names), fetch_all=True)
        
        return [
            {
                "name": row[0],
                "minlong": row[1],
                "minlat": row[2],
                "maxlong": row[3],
                "maxlat": row[4],
            }
            for row in rows
        ] if rows else []

    def add(self, name: str, minlong: float, minlat: float, maxlong: float, maxlat: float):
        """Add a new suburb to the database."""
        query = """
        INSERT INTO suburbs (name, minlong, minlat, maxlong, maxlat)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (name, minlong, minlat, maxlong, maxlat))

    def add_many(self, suburbs: List[Dict[str, str]]):
        """Batch insert multiple suburbs."""
        query = """
        INSERT INTO suburbs (name, minlong, minlat, maxlong, maxlat)
        VALUES %s
        """
        values = [(s["name"], s["minlong"], s["minlat"], s["maxlong"], s["maxlat"]) for s in suburbs]
        args_str = ",".join(self.db.cur.mogrify("(%s, %s, %s, %s, %s)", x).decode() for x in values)
        self.db.execute_query(query % args_str)
