from typing import List, Dict
import json

class Road:
    def __init__(self, db):
        self.db = db  # Store the database instance

    def get_by_name(self, name: str, suburb: str) -> Dict:
        """Fetch a suburb by name."""
        query = "SELECT id, name, suburb, points FROM roads WHERE name = %s AND suburb ="
        row = self.db.execute_query(query, (name, suburb,), fetch_one=True)
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "suburb": row[2],
                "points": row[3]
            }
        return None

    def get_by_names(self, names):
        """Fetch multiple suburbs by a list of (name, suburb) pairs."""
        if not names:
            return []

        conditions = " OR ".join(["(name = %s AND suburb = %s)" for _ in names])
        
        query = f"""
            SELECT id, name, suburb, points 
            FROM roads 
            WHERE {conditions}
        """

        flattened_names = [item for sublist in names for item in sublist]  # Flatten the list

        rows = self.db.execute_query(query, tuple(flattened_names), fetch_all=True)

        return [
            {
                "id": row[0],
                "name": row[1],
                "suburb": row[2],
                "points": row[3]
            }
            for row in rows
        ] if rows else []



    def add(self, name: str, suburb: str, points):
        """Add a new suburb to the database."""
        query = """
        INSERT INTO roads (name, suburb, points)
        VALUES (%s, %s, %s)
        """
        self.db.execute_query(query, (name, suburb, json.dumps(points)))

    def add_many(self, roads: List[Dict[str, str]]):
        """Batch insert multiple suburbs."""
        query = """
        INSERT INTO roads (name, suburb, points)
        VALUES %s
        """
        args = ", ".join([str((r["name"], r["suburb"], json.dumps(r["points"]))) for r in roads])
        self.db.execute_query(query % args)
