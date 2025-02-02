import datetime
import logging
import azure.functions as func
import requests
from bs4 import BeautifulSoup

app = func.FunctionApp()

@app.function_name(name="MonthlyTrigger")
@app.schedule(schedule="0 0 1 * * *", arg_name="myTimer", run_on_startup=True, use_monitor=True)
def main(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    logging.info(f"Function triggered at {utc_timestamp}")

    # Web scraping code
    url = 'https://www.vic.gov.au/mobile-phone-and-seatbelt-detection-camera-locations'
    try:
        # Send HTTP request to the website
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Example: Extract all headings <h1> from the page
            headings = soup.find_all('h1')

            # Log the headings (you can also save them to a file or database)
            for heading in headings:
                logging.info(f"Found heading: {heading.text}")
        else:
            logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error while fetching the website: {e}")
