import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PRICES_ENDPOINT = os.getenv("PRICES_ENDPOINT")
USERS_ENDPOINT = os.getenv("USERS_ENDPOINT")

class DataManager:
    """This class is responsible for talking to the Google Sheet."""
    def __init__(self):
        self._token = os.getenv("SHEETY_TOKEN")
        self.header = {"Authorization": f"Bearer {self._token}"}
        self.destination_data = []
        self.users_data = []

    def get_prices_data(self):
        """
        Function makes GET request to Sheety endpoint and obtain prices/destination data from Google Sheet.

        :return: Destination data from Google Worksheet
        """
        response = requests.get(url=PRICES_ENDPOINT, headers=self.header)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """
        FUnction updates IATA codes in Google Worksheet of cities if any are missing.

        :return: None
        """
        for row in self.destination_data:
            new_data = {
                    "price": {"iataCode": row["iataCode"]}
            }
            response = requests.put(url=f"{PRICES_ENDPOINT}/{row["id"]}", headers=self.header, json=new_data)
            response.raise_for_status()

    def get_customer_emails(self):
        """
        Function makes GET request to Sheety endpoint and obtain users data from Google Sheet.

        :return: List of users data from Google Worksheet
        """
        response = requests.get(url=USERS_ENDPOINT, headers=self.header)
        response.raise_for_status()
        self.users_data = response.json()["users"]
        return self.users_data
