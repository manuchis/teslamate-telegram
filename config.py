import os

if os.getenv('MQTT_SERVER') == None:
    print("Error: Please set the environment variable MQTT_SERVER and try again.")
    exit(1)
if os.getenv('MQTT_PORT') == None:
    print("Error: Please set the environment variable MQTT_PORT and try again.")
    exit(1)
if os.getenv('BOT_TOKEN') == None:
    print("Error: Please set the environment variable BOT_TOKEN and try again.")
    exit(1)
if os.getenv('BOT_CHAT_ID') == None:
    print("Error: Please set the environment variable BOT_CHAT_ID and try again.")
    exit(1)
    
MQTT_SERVER = os.getenv('MQTT_SERVER')
MQTT_PORT = os.getenv('MQTT_PORT')
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_CHAT_ID = os.getenv('BOT_CHAT_ID')
OPTIONS = os.getenv('OPTIONS')
CAR_ID = os.getenv('CAR_ID')
SEND_RESUME = os.getenv('SEND_RESUME')
DEBUG = os.getenv('DEBUG')
