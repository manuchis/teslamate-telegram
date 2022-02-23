#!/bin/sh
if [ -n "$MQTT_SERVER" ]; then
  echo "MQTT_SERVER = $MQTT_SERVER" > config.py
fi

if [ -n "$MQTT_PORT" ]; then
  echo "MQTT_PORT = $MQTT_PORT" >> config.py
fi

if [ -n "$BOT_TOKEN" ]; then
  echo "BOT_TOKEN = $BOT_TOKEN" >> config.py
fi

if [ -n "$BOT_CHAT_ID" ]; then
  echo "BOT_CHAT_ID = $BOT_CHAT_ID" >> config.py
fi

if [ -n "$OPTIONS" ]; then
  echo "OPTIONS = $OPTIONS" >> config.py
fi

if [ -n "$CAR_ID" ]; then
  echo "CAR_ID = $CAR_ID" >> config.py
fi

if [ -n "$SEND_RESUME" ]; then
  echo "SEND_RESUME = $SEND_RESUME" >> config.py
fi

if [ -n "$DEBUG" ]; then
  echo "DEBUG = $DEBUG" >> config.py
fi
exec "$@"
