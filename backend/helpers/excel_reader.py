import pandas as pd
from fastapi import HTTPException
from models.CameraTypeEnum import CameraType

def get_road_suburb_from_excel(url: str, type: CameraType):
    road_suburb_list = []
    try:
        print(url)
        # Use 'openpyxl' engine for .xlsx files
        df = pd.read_excel(url, engine='openpyxl')
        print("Downloaded")
        print(df.head())
        column_names = list(df.columns)
        for index, row in df.iterrows():
            # Get the values of the first two columns
            road_suburb = (row[column_names[0]], row[column_names[1]], type)
            road_suburb_list.append(road_suburb)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")
    return road_suburb_list
