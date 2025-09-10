import os
import requests

AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1"
TOKEN_ENDPOINT = f"{AMADEUS_ENDPOINT}/security/oauth2/token"
CITIES_ENDPOINT = f"{AMADEUS_ENDPOINT}/reference-data/locations/cities"
OFFERS_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET_KEY"]
        self._token = self._get_new_token()
        self._authorization = {
            "Authorization": f"Bearer {self._token}"
        }

    def _get_new_token(self):
        """
        Funtion makes POST request to Amadeus token endpoint to obtain a new client credentials token.

        :return: str: The new access token taken from the API response
        """


        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        return response.json()["access_token"]

    def search_IATA_code(self, city):
        """
        Retrieves the IATA code for a specified city using the Amadeus Location API.

        :param city: name of the city for which to find IATA code
        :return: str: IATA code for the first matching city; "N/A" if no match found due to IndexError;
        "Not Found" if no match found due to KeyError
        """

        parameters = {
            "keyword" : city
        }

        response = requests.get(url=CITIES_ENDPOINT, headers=self._authorization, params=parameters)

        try:
            city_code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return city_code

    def find_flights(self,
                     originLocationCode,
                     destinationLocationCode,
                     departureDate,
                     returnDate,
                     adults,
                     is_direct,
                     currencyCode,
                     offers_limit="10"):
        """
        Function makes GET request to retrieve flight offers for particular destination.


        :param originLocationCode:
        :param destinationLocationCode:
        :param departureDate:
        :param returnDate:
        :param adults:
        :param is_direct:
        :param currencyCode:
        :param offers_limit: OPTIONAL, default: 10
        :return: Dictionary with maximum number of flight offers
        """

        parameters = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode":destinationLocationCode,
            "departureDate":departureDate,
            "returnDate":returnDate,
            "adults":adults,
            "nonStop": "true" if is_direct else "false",
            "currencyCode":currencyCode,
            "max": offers_limit
        }
        response = requests.get(url=OFFERS_ENDPOINT, headers=self._authorization, params=parameters)

        # Return None if something happened with request
        if response.status_code != 200:
            print(f"find_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()