class FlightData:
    """This class is responsible for structuring the flight data."""
    def __init__(self,
                 price = "N/A",
                 origin_airport = "N/A",
                 destination_airport = "N/A",
                 out_date = "N/A",
                 return_date = "N/A",
                 stops = 0):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    def print(self):
        print(f"{self.destination_airport}: £{self.price}")

def find_cheapest_flight(data):
    """
    Function loops through FlightData object and searches for the cheapest flight offer (total flight price).

    :param data: dictionary
    :return: FlightData object
    """

    if data is None or not data["data"]:
        print("No flight data")
        return FlightData()

    first_flight = data['data'][0]

    lowest_price = float(first_flight["price"]["grandTotal"])
    origin_airport = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    nr_stops = len(first_flight["itineraries"][0]["segments"])-1
    destination_airport = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    departure_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][nr_stops]["arrival"]["at"].split("T")[0]

    lowest_flight = FlightData(lowest_price, origin_airport, destination_airport,
                               departure_date, return_date, nr_stops)

    for flight in data['data'][1:]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_flight.price:
            lowest_price = flight["price"]["grandTotal"]
            origin_airport = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
            destination_airport = flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
            departure_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][nr_stops]["arrival"]["at"].split("T")[0]

            lowest_flight=FlightData(lowest_price,
                                     origin_airport,
                                     destination_airport,
                                     departure_date,
                                     return_date,
                                     nr_stops)

    return lowest_flight