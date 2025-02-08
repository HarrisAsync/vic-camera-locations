import pandas as pd
from fastapi import HTTPException
from models.CameraTypeEnum import CameraType
import requests
import openpyxl
from io import BytesIO
def get_road_suburb_from_excel(url: str, type: CameraType):
    try:
        print(url)
        # Step 1: Download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request failed

        # Step 2: Load the workbook from memory
        excel_data = BytesIO(response.content)
        workbook = openpyxl.load_workbook(excel_data, data_only=True)

        # Step 3: Choose the first worksheet (or pick by name)
        sheet = workbook.worksheets[0]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")
    return [(row[0], row[1], type) for row in sheet.iter_rows(values_only=True)[1:]]
