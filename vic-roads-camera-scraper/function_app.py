import datetime
import logging
import azure.functions as func
import requests
from bs4 import BeautifulSoup
import os
import re

app = func.FunctionApp()

@app.function_name(name="EveryTwoDaysTrigger")
@app.schedule(schedule="0 0 */2 * * *", arg_name="myTimer", run_on_startup=True, use_monitor=True)
def main(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    logging.info(f"Function triggered at {utc_timestamp}")

    # Get the URLs from the settings
    base_url = os.getenv('Base_Url')
    mobile_PHST_url = base_url + os.getenv('Mobile_Phone_Seatbelt_Camera_Url')
    mobile_SPD_url = base_url + os.getenv('Mobile_Speed_Camera_Url')
    public_key = os.getenv('Public_Key')
    endpoint = os.getenv('Backend_Endpoint')

    # Define regex patterns
    pattern_mobile_PHST = r"(?i).*(DDS|location|camera).*\.xlsx$"
    pattern_mobile_SPD = r"(?i).*(location|camera).*\.xlsx$"

    # Get the excel sheet from the urls
    link_PHST = base_url + get_sheet_link(mobile_PHST_url, pattern_mobile_PHST)
    link_SPD = base_url + get_sheet_link(mobile_SPD_url, pattern_mobile_SPD)

    logging.info(f"link_PHST: {link_PHST}")
    logging.info(f"link_SPD: {link_SPD}")

    # Post links to enpoint
    data = {
        "link_PHST": link_PHST,
        "link_SPD": link_SPD,
        "public_key": public_key
    }

    if (data["link_PHST"] == "" and data["link_SPD"] == ""):
        return

    try:
        # Post to endpoint
        response = requests.post(endpoint, json=data)
        logging.info(f"Post Response: {response}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error while posting: {e}")


def get_sheet_link(url, pattern):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link['href']
                match = re.search(pattern, href)
                if match:
                    return href
        else:
            logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error while fetching the website: {e}")
    return ""
