#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from twilio.rest import Client
import random
import re
import requests
import time
import yaml

start_time = time.perf_counter()
# Crawl volunteer website 
URL = "https://www.voly.org/opportunity/view.html?id=62211"
req = requests.get(URL)
only_divs = SoupStrainer("div")
soup = BeautifulSoup(req.content, 'lxml', parse_only=only_divs)
todays_needs = soup.find_all(class_="action-spacing")

# Grab volunteer information
date = todays_needs[0].get_text()
shift_hours = todays_needs[1].get_text()
num_volunteers = re.findall(r'\d+', todays_needs[2].get_text())

# Clean volunteer information
date = date.strip()
shift_hours = shift_hours.strip()
num_volunteers = int(num_volunteers[0])

print("Collected volunteer information:")
print(f"date: {date}\nshift hours: {shift_hours}\nnum_volunteers: {num_volunteers}\n")

# Check if there are volunteer spots for the day
if num_volunteers > 0:

    # Load configuration and set variables
    config = yaml.safe_load(open("./config/configuration.yaml"))
    account_sid = config["twilio"]["account_sid"]
    auth_token = config["twilio"]["auth_token"]
    account_phone_number = config["twilio"]["account_phone_number"]
    phone_book = config["phone_book"]
    random.shuffle(phone_book)
    message_body = f"Howdy!\n\n" \
        f"This is an alert to let you that there are currently {num_volunteers} opening(s) " \
        f"to volunteer at the Dallas County Vaccine Mega Center on {date}. The shift(s) will most likely last {shift_hours}.\n\n" \
        f"If you are interested, please sign up at {URL}\n\n" \
        f"Please do not reply to this message. Good luck!"
    
    print("YAML configuration variables loaded")
    print()

    # Create Twilio Client
    client = Client(account_sid, auth_token)
    print("Twilio Client created")
    print()

    # Send texts to all phone numbers 
    for phone_number in phone_book:
        message = client.messages \
            .create(
                body = message_body,
                from_ = account_phone_number,
                to = phone_number
            )

end_time = time.perf_counter()
print(f"Retrieved information and sent out alerts in {end_time - start_time:0.4f} seconds")
