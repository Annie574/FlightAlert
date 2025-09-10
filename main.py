import time
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight


# =============== Set up the Flight Search ===============

# Set your preferences if needed
ORIGIN_CITY_CODE = "LON" # IATA code
DIRECT_FLIGHT = True
TIME_PERIOD = 30*6 # 6 months
ADULTS = 1
CURRENCY = "GBP"

manager = DataManager()
flight_manager = FlightSearch()
notification_manager = NotificationManager()

# =============== Update IATA codes in Google Sheet ===============
sheet_data = manager.get_prices_data()

for row in sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_manager.search_IATA_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)

manager.destination_data = sheet_data
manager.update_destination_codes()

# =============== Obtain users database from Google Sheet ===============

users_data = manager.get_customer_emails()
customer_email_list = [row["whatIsYourEmail?"] for row in users_data]
# print(f"Your email list includes {customer_email_list}")

# =============== SEARCH FO FLIGHT OFFERS AND NOTIFY ===============

tomorrow = datetime.today() + timedelta(days=1)
time_period_end = (tomorrow + timedelta(days=TIME_PERIOD))

for row in sheet_data:
    print(f"Getting flights for {row["city"]}...")
    flights_available = flight_manager.find_flights(ORIGIN_CITY_CODE,
                                                    row["iataCode"],
                                                    tomorrow.strftime("%Y-%m-%d"),
                                                    time_period_end.strftime("%Y-%m-%d"),
                                                    ADULTS,
                                                    DIRECT_FLIGHT,
                                                    CURRENCY)
    if not flights_available["data"] and DIRECT_FLIGHT is True:
        print(f"No direct flights from {ORIGIN_CITY_CODE} to {row["iataCode"]}.")
        print(f"Getting indirect flights for {row["city"]}...")
        flights_available = flight_manager.find_flights(ORIGIN_CITY_CODE,
                                                    row["iataCode"],
                                                    tomorrow.strftime("%Y-%m-%d"),
                                                    time_period_end.strftime("%Y-%m-%d"),
                                                    ADULTS,
                                                    False,
                                                    CURRENCY)

    cheapest_flight = find_cheapest_flight(flights_available)

    print(f"{row["city"]}: £{cheapest_flight.price}")
    if cheapest_flight.price != "N/A" and cheapest_flight.price < row["lowestPrice"]:
        # notification_manager.send_notification_sms(cheapest_flight)
        notification_manager.send_emails(cheapest_flight, customer_email_list)
