import pandas as pd
from fastapi import HTTPException
from models.CameraTypeEnum import CameraType

def get_road_suburb_from_excel(file_path: str, type: CameraType):
    road_suburb_list = []
    try:
        df = pd.read_excel(file_path)
        column_names = list(df.columns)
        for row in df.iterrows():
            road_suburb = (row[column_names[0]], row[column_names[1]], type)
            road_suburb_list.append(road_suburb)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")
    return road_suburb_list