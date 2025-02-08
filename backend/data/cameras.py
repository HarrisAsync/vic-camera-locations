from typing import List, Dict
import json

class Camera:
    def __init__(self, db):
        self.db = db  # Store the database instance

    def get_all(self, type=None):
        """Fetch a suburb by name."""
        if type == None:
            query = "SELECT cameras.id, camera_type, points, roads.name, roads.suburb FROM cameras JOIN roads on cameras.road_id = roads.id"
        else:
            query = f"SELECT cameras.id, camera_type, points, roads.name, roads.suburb FROM cameras JOIN roads on cameras.road_id = roads.id WHERE camera_type = {int(type)}"
        rows = self.db.execute_query(query, fetch_one=False, fetch_all=True)
        return [
            {
                "id": row[0],
                "camera_type": row[1],
                "points": row[2],
                "road": row[3],
                "suburb": row[4]
            }
            for row in rows
        ] if rows else []

    def set_new(self, cameras):
        self.db.execute_query("DELETE FROM cameras")
        query = "INSERT INTO cameras (camera_type, road_id) VALUES (%s, %s)"
        
        # Convert list of dicts to tuples
        values = [(cam["camera_type"], cam["road_id"]) for cam in cameras]

        # Execute batch insert
        self.db.cur.executemany(query, values)
        self.db.conn.commit()  # Commit the transaction
    