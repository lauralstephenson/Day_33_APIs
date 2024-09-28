# This is a file that links to an API 
# To tell the user if the ISS is overhead
# Replace with your own email and email password

import requests
from datetime import datetime
import smtplib
import time

#Warning: If your computer is on and this code is running, it will run every sixty seconds forever.

#My email settings
MY_EMAIL = "your_email_here"
MY_PASSWORD = "your_password_here"
#Getting the sunrise where I live
MY_LAT = 35.136361
MY_LONG = 129.098109

#IF the ISS is close to my position and it is currently dark
#Then send me an email to tell me to look up.
#Close to is +5 or -5 degrees of my position

def is_iss_overhead():
    # How to find where the ISS is located using its API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        # Use smtplib to send the email to yourself
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: Look up☝️\n\nThe ISS is above you in the sky!"
            )
