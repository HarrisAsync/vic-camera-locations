from fastapi import HTTPException
import requests
import openpyxl
from io import BytesIO

def get_road_suburb_from_excel(url: str, type: CameraType) -> list[tuple]:
    try:
        print("Parsing url" + url)
        # Step 1: Download the file
        response = requests.get(url)

        response.raise_for_status()  # Raise an exception if the request failed

        # Step 2: Load the workbook from memory
        excel_data = BytesIO(response.content)
        workbook = openpyxl.load_workbook(excel_data, data_only=True)

        # Step 3: Choose the first worksheet (or pick by name)
        sheet = workbook.worksheets[0]


        # Step 4: Read rows.
        # Skip first 2 rows
        list_roads_suburbs = []
        for row in sheet.iter_rows(min_row=3):
            if row[0].value == None:
                break
            list_roads_suburbs.append((double_up_apostrophe(row[0].value), double_up_apostrophe(row[1].value), type))

        return list_roads_suburbs
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")


def double_up_apostrophe(string: str):
    out = ''
    for c in string:
        if c == "'":
            out += c + c
        else:
            out += c
    return out