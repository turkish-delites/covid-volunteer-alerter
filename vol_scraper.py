#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from twilio.rest import Client
from datetime import datetime
import random
import requests
import time
import yaml

start_time = time.perf_counter()
print("Started vol_scraper.py")

# Crawl volunteer website 
URL = "https://www.voly.org/opportunity/volunteer.html?id=62211"
req = requests.get(URL)
cal_buttons = SoupStrainer("button", {"class": "button__full-width button__primary volunteerCalendar__button--recurring is-active"})
soup = BeautifulSoup(req.content, 'lxml', parse_only=cal_buttons)
cal_dates = soup.find_all("span", ["volunteerCalendar__date", "volunteerCalendar__count"])
# print(cal_dates)
# print()

# Grab volunteer availabilities for the current month from calendar
date_index_list = []
for i in range(0, len(cal_dates), 2):
    if int(cal_dates[i+1].get_text()) > 0:
        date_index_list.append(i)

# print(f"len(date_index_list): {len(date_index_list)}")

# Send out alerts if there are volunteer opportunities for the month
if len(date_index_list) > 0:
    # Calculate total number of volunteer shifts
    total_shifts = 0
    for i in date_index_list:
        total_shifts += int(cal_dates[i+1].get_text())

    # Load configuration and set variables
    config = yaml.safe_load(open("./config/configuration.yaml"))
    account_sid = config["twilio"]["account_sid"]
    auth_token = config["twilio"]["auth_token"]
    account_phone_number = config["twilio"]["account_phone_number"]
    phone_book = config["phone_book"]
    random.shuffle(phone_book)
    message_body = f"Howdy!\n\n" \
        f"This is an alert to let you that there is(are) currently {total_shifts} opening(s) " \
        f"to volunteer at the Dallas County Vaccine Mega Center this month.\n\n" \
        f"If you are interested, please sign up at {URL}\n\n" \
        f"Please do not reply to this message. Good luck!"
    
    print("YAML configuration variables loaded")

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
    
    # Print shift info
    print(f"total_shifts: {total_shifts}")
    curr_year = datetime.now().year
    curr_month = datetime.now().month
    for i in date_index_list:
        print(f"Date: {curr_year}-{curr_month}-{cal_dates[i].get_text()}, Num of Volunteers Needed: {cal_dates[i+1].get_text()}")
else:
    print("No volunteer shifts available")

end_time = time.perf_counter()
print(f"Retrieved information and sent out alerts in {end_time - start_time:0.4f} seconds")
print()
