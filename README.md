# Dallas County COVID-19 Mass Vaccination Volunteer Alerter

This repo contains a python script that scrapes the Dallas County COVID-19 Mass Vaccination voly.org volunteer page in order to send out text alerts via Twilio when volunteer spots become available.
<br/><br/>

## Usage

This project is intended to be used as cron job that will run every 5 minutes on a Raspberry Pi that I own. However, it could be easily configured to run in the cloud if desired.
<br/><br/>

## Installation

Just download the project from GitHub, unzip and run it as a normal Python script for any Unix based system (MacOS/Linux). Instructions to utilize the Twilio SMS API can be found [here](https://www.twilio.com/docs/sms/quickstart/python)

Make sure to also create a `./config/configuration.yaml` file with the following structure:

```yaml
---
twilio:
    account_sid: ""
    auth_token: ""
    account_phone_number: ""

phone_book:
    - ""
```

<br/>

## Versions

-   **v1.0:** Only scrapes the data available for today's date. Sends alerts out to all phone numbers collected in the phone book.
    <br/><br/>

## License

[MIT](LICENSE.txt)
