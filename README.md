# TeslaMate to Telegram

[![](https://img.shields.io/badge/Donate-PayPal-ff69b4.svg)](https://www.paypal.com/donate?hosted_button_id=9H6B9CRBL6V4E)

Script that collects data from the Teslamate via MQTT and sends messages to a Telegram chatbot.

### Requirements

* For python version: Python 2.7+ & Install dependencies of Python included in requirements.txt
* For Docker version: Docker (if running in a docker container)
* To obtain your Telegram [API bot token](https://core.telegram.org/bots#6-botfather)
* To obtain your Telegram [chat ID](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id)

### Instructions for running on Docker


1. Create a file called `docker-compose.yml` with the following content (adopt with your own values - see descriptions in python version):

   ```yml title="docker-compose.yml"
version: "3"

services:
  teslamatemqtttotelegram:
    image: teslamatemqtttotelegram/teslamatemqtttotelegram:latest
    restart: unless-stopped
    environment:
     - MQTT_SERVER = 
     - MQTT_PORT =
     - BOT_TOKEN =
     - BOT_CHAT_ID =
     - OPTIONS = update_version
     - CAR_ID = 1
     - SEND_RESUME = True
     - DEBUG = True
   ports:
     - 1883
   build:
     context: .
     dockerfile: Dockerfile
   ```

2. Build and start the docker container with `docker-compose up`. To run the containers in the background add the `-d` flag:

   ```bash
   docker-compose up -d
   ```

### Instructions for running directly on python

1. Install all dependencies of Python
~~~
pip install -r requirements.txt
~~~
2. Replace the `config.py` file with the variables of your MQTT of Teslamate and ABRP inside `config.py` file
~~~
MQTT_SERVER = "@@@@@@@@"                              # MQTT server address (e.g. "127.0.0.1")
MQTT_PORT = "@@@@"                                    # MQTT server port (e.g. "1883")
BOT_TOKEN = "@@@@@@@@@@:@@@@@@@@@@@@@@@@@@@@"         # Bot token
BOT_CHAT_ID = "@@@@@@@@@@"                            # Chat ID
OPTIONS = "update_version"                            # Select options to send notification (options: state, update_version, display_name, (e.g. "state|update_version"))  
CAR_ID = "1"                                          # Car number (usually 1 if you only have a car)
SEND_RESUME = True/False                              # Enable or disable resume when state change to sleep
DEBUG = True/False                                    # Enable or disable debug mode
~~~
4. Run the script
* Run on command line (ideal for testing)
~~~
python ./teslamateMqttToTelegram.py
~~~
* Run in the background
~~~
nohup python ./teslamateMqttToTelegram.py & > /dev/null 2>&1
~~~+


## Credits

- Authors: Carlos Cuezva – [List of contributors](https://github.com/carloscuezva/teslamate-telegram/graphs/contributors)
- Distributed under MIT License
