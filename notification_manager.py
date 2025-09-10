import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv()

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self):
        self._account_sid = os.getenv("TWILIO_ID")
        self._auth_token = os.getenv("TWILIO_TOKEN")
        self.client = Client(self._account_sid, self._auth_token)
        self.sender_number = os.getenv("VIRTUAL_NUMBER")
        self.alert_number = os.getenv("PERSONAL_NUMBER")
        self._mail_account = os.getenv("MY_MAIL")
        self._mail_password = os.getenv("MY_PASSWORD")


    def send_notification_sms(self, flight: FlightData):
        """
        Function sends notification from TWILIO virtual number

        :param flight:
        :return: None
        """

        message = self.client.messages.create(
            body=f"Low price alert! Only {flight.price} to fly from {flight.origin_airport} "
                 f"to {flight.destination_airport}, on {flight.out_date} until {flight.return_date}.",
            from_=self.sender_number,
            to=self.alert_number
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, flight: FlightData, mailing_list: list):

        if flight.stops == 0:
            itineraries = "direct one!"
        else:
            itineraries = f"only {flight.stops} stop(s)!"

        message = (f"Only {flight.price} to fly from {flight.origin_airport} "
                   f"to {flight.destination_airport} ({itineraries}), "
                   f"departing on {flight.out_date} and returning on {flight.return_date}.")

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self._mail_account, password=self._mail_password)
            for mail_address in mailing_list:
                connection.sendmail(
                    from_addr=self._mail_account,
                    to_addrs=mail_address,
                    msg=f"Subject:New Low Price alert!\n\n{message}".encode("utf-8")
                )