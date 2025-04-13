import os
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from utils.logger import logging

# URL of the page with the CSV download link
page_url = os.getenv("GOVT_PAGE_URL", None)

def get_csv_download_link():
    """
    Extracts the CSV download link from the UK Government's page.
    Returns the URL to the CSV file.
    """
    logging.info(f"Scraping the page for the CSV download link: {page_url}")

    try:
        # Fetch the page content
        response = requests.get(page_url, timeout=10)

        if response.status_code != 200:
            logging.error(f"Failed to retrieve page. Status code: {response.status_code}")
            raise Exception(f"Failed to retrieve page. HTTP Status Code: {response.status_code}")

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the link to the CSV file (the actual link is often in an anchor tag with a specific text)
        # download_link = None
        # for link in soup.find_all("a", href=True):
        #     if "download" in link.get("href", "").lower() and "csv" in link.get_text().lower():
        #         download_link = link["href"]
        #         break

        a_tag = soup.find("a", {
            'class': 'govuk-link gem-c-attachment__link',
            'target': '_self'
        })

        download_link = a_tag["href"] if a_tag is not None else None

        # ✅ Check if the link ends with .csv
        if not download_link.lower().endswith(".csv"):
            logging.error(f"Invalid CSV download link (does not end with .csv): {download_link}")
            raise Exception("Invalid CSV download link: URL does not end with .csv")

        if not download_link:
            logging.error("CSV download link not found on the page.")
            # Report an email
            raise Exception("CSV download link not found on the page.")

        # Ensure the download link is absolute
        if not download_link.startswith("http"):
            download_link = "https://www.gov.uk" + download_link

        logging.info(f"CSV download link found: {download_link}")
        return download_link

    except Exception as e:
        logging.error(f"An error occurred while scraping the page: {str(e)}")
        raise

def download_latest_csv():
    """
    Downloads the latest CSV file from the UK Gov Sponsor Licence register.
    Returns the file path to the downloaded CSV.
    """
    try:
        # Set up filename with today's date (ignore time)
        today_str = datetime.now().strftime("%Y-%m-%d")
        download_dir = './data/raw'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Look for an existing file for today
        for file in os.listdir(download_dir):
            if file.startswith(f"uk_sponsor_register_{today_str}"):
                existing_file_path = os.path.join(download_dir, file)
                logging.info(f"✅ Today's CSV already exists: {existing_file_path}")
                return existing_file_path

        # Get the actual CSV download link
        csv_url = get_csv_download_link()

        # Set up filename with timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        download_dir = './data/raw'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        file_name = f"uk_sponsor_register_{timestamp}.csv"
        file_path = os.path.join(download_dir, file_name)

        # Download the CSV file
        logging.info(f"Downloading CSV file from {csv_url}...")

        response = requests.get(csv_url, timeout=10)

        if response.status_code == 200:
            # Save the CSV to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"File downloaded successfully: {file_path}")

            # Load the CSV into a pandas DataFrame to validate the contents
            data = pd.read_csv(file_path)
            logging.info(f"Downloaded CSV contains {len(data)} rows and {len(data.columns)} columns.")

            return file_path
        else:
            logging.error(f"Failed to download CSV. Status code: {response.status_code}")
            raise Exception(f"Failed to download CSV. HTTP Status Code: {response.status_code}")

    except Exception as e:
        logging.error(f"An error occurred while downloading the CSV: {str(e)}")
        raise
