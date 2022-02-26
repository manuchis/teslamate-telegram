# -*- coding: utf-8 -*-
import os
import requests
import sys
from time import sleep
import telebot
import teslapy
from datetime import datetime
from datetime import timedelta

import os

if os.getenv('USER_EMAIL') == None:
    print("Error: Please set the environment variable USER_EMAIL and try again.")
    exit(1)
else:
    USER_EMAIL = os.getenv('USER_EMAIL')
if os.getenv('BOT_TOKEN') == None:
    print("Error: Please set the environment variable BOT_TOKEN and try again.")
    exit(1)
else:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
if os.getenv('BOT_CHAT_ID') == None:
    print("Error: Please set the environment variable BOT_CHAT_ID and try again.")
    exit(1)
else:
    BOT_CHAT_ID = os.getenv('BOT_CHAT_ID')

with teslapy.Tesla(USER_EMAIL) as tesla:
    if not tesla.authorized:
        tesla.refresh_token(refresh_token=input('Enter SSO refresh token: '))
    vehicles = tesla.vehicle_list()
    print(vehicles[0].get_vehicle_summary())

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def blue_command(message):

   keyboard = telebot.types.InlineKeyboardMarkup()

   keyboard.row(
                telebot.types.InlineKeyboardButton('Estado',callback_data='status'),
                telebot.types.InlineKeyboardButton('Despertar',callback_data='wake_up'),
                telebot.types.InlineKeyboardButton('Resumen vehículo',callback_data='vehicle_summary'),
                telebot.types.InlineKeyboardButton('Info',callback_data='info')
               )

   keyboard.row(
                telebot.types.InlineKeyboardButton('Activar sentry',callback_data='sentry_on'),
                telebot.types.InlineKeyboardButton('Desactivar sentry',callback_data='sentry_off')
               )

   keyboard.row(
                telebot.types.InlineKeyboardButton('Abrir p. carga',callback_data='unlock_charge_port'),
                telebot.types.InlineKeyboardButton('Cerrar p. carga',callback_data='lock_charge_port'),
                telebot.types.InlineKeyboardButton('Iniciar carga',callback_data='start_charge'),
                telebot.types.InlineKeyboardButton('Parar carga',callback_data='stop_charge')
               )

   keyboard.row(
                telebot.types.InlineKeyboardButton('50%',callback_data='charge50'),
                telebot.types.InlineKeyboardButton('55%',callback_data='charge55'),
                telebot.types.InlineKeyboardButton('60%',callback_data='charge60'),
                telebot.types.InlineKeyboardButton('65%',callback_data='charge65'),
                telebot.types.InlineKeyboardButton('70%',callback_data='charge70'),
                telebot.types.InlineKeyboardButton('75%',callback_data='charge75'),
                telebot.types.InlineKeyboardButton('80%',callback_data='charge80'),
                telebot.types.InlineKeyboardButton('85%',callback_data='charge85'),
                telebot.types.InlineKeyboardButton('90%',callback_data='charge90'),
                telebot.types.InlineKeyboardButton('95%',callback_data='charge95'),
                telebot.types.InlineKeyboardButton('100%',callback_data='charge100')
               )

   keyboard.row(
                telebot.types.InlineKeyboardButton('10A',callback_data='amp10'),
                telebot.types.InlineKeyboardButton('16A',callback_data='amp16'),
                telebot.types.InlineKeyboardButton('20A',callback_data='amp20'),
                telebot.types.InlineKeyboardButton('25A',callback_data='amp25'),
                telebot.types.InlineKeyboardButton('32A',callback_data='amp32')
               )

   bot.send_message(message.chat.id,'¡Hola!',reply_markup=keyboard)

def get_callback(query):

   mi = 1.6093345204294200621295255350501

   with teslapy.Tesla(USER_EMAIL) as tesla:
       if not tesla.authorized:
           tesla.refresh_token(refresh_token=input('Enter SSO refresh token: '))
       vehicles = tesla.vehicle_list()
       vehicle_summary = vehicles[0].get_vehicle_summary()

   bot.answer_callback_query(query.id)

   if query.data == 'wake_up':
       print('Despertando...')
       vehicles[0].sync_wake_up()
       bot.send_message(query.message.chat.id,'🆙')
       print('Despierto')
       return

   if query.data == 'status':
       vehicles = tesla.vehicle_list()
       vehicle_summary = vehicles[0].get_vehicle_summary()

       if vehicle_summary["state"] == 'online':
           estado = 'Despierto'
       if vehicle_summary["state"] == 'asleep':
           estado = 'Dormido'
       if vehicle_summary["state"] == 'suspended':
           estado = 'Dormido'
       if vehicle_summary["state"] == 'offline':
           estado = 'No disponible'
       print('Estado: '+estado)

       bot.send_message(query.message.chat.id,estado)
       return

   if query.data == 'vehicle_summary':
      vehicle_summary = vehicles[0].get_vehicle_summary()
      for i in vehicle_summary:
          if vehicle_summary[i]:
             bot.send_message(query.message.chat.id,vehicle_summary[i])
      return

   if vehicle_summary["state"] != 'online':
      bot.send_message(query.message.chat.id,"Coche no despierto, hay que despertarlo primero")
      return

   if query.data == 'info':
       vehicle_data = vehicles[0].get_vehicle_data()
       charge = vehicle_data['charge_state']
       climate = vehicle_data["climate_state"]
       state = vehicle_data["vehicle_state"]

       if vehicle_data["state"] == 'online':
           estado = 'Despierto'
       if vehicle_data["state"] == 'asleep':
           estado = 'Dormido'
       if vehicle_data["state"] == 'offline':
           estado = 'No disponible'

       if state["locked"]:
           locked = "🔐  Cerrado"
       else:
           locked = "🔓  Abierto"

       if charge["usable_battery_level"] != charge["battery_level"]:
          bat = "Usable {0}% (disponible {1}%) {2:.0f} km".format(charge["usable_battery_level"],charge["battery_level"],round(charge["battery_range"]*mi,0))
       else:
          bat = "Disponible {0}% {1:.0f} km".format(charge["usable_battery_level"],round(charge["battery_range"]*mi,0))

       limite = charge["charge_limit_soc"]

       if charge["charging_state"] == "Charging":
          horas = int(charge["time_to_full_charge"])
          minutos = (charge["time_to_full_charge"] - horas) * 60
          total_minutos = horas * 60 + minutos
          intensidad = charge["charge_amps"]
          voltaje =  charge["charger_voltage"]
          fases = charge["charger_phases"]
          hora_actual = datetime.now()
          hora_fin_carga = hora_actual + timedelta(minutes=total_minutos)

          if fases == 1:
             potencia = round(voltaje * intensidad / 1000,1)
             modo_carga = "monofásica"
          else:
             if voltaje != 2:
                modo_carga = "trifásica"
                potencia = round(3 * voltaje * intensidad / 1000,1)
             else:
                modo_carga = "continua"
                potencia =  charge["charger_power"]

          estado = estado + " (cargando en " + modo_carga + " a {:.1f} kW)".format(potencia)

       if state["sentry_mode"]:
          sentry = '🔴 ACTIVADO'
       else:
          sentry = '🔘 Desactivado'

       text = " *** Estado de " + state["vehicle_name"] + " ***" \
              + "\n\n    💿  " + state["car_version"].split()[0] \
              + "\n    🚗  " + estado \
              + "\n    ⚙️  {:.0f} km".format(round(state["odometer"]*mi),0) \
              + "\n    " + locked \
              + "\n    🔋  {}".format(bat) \
              + "\n    ⏱  Límite de carga {}%".format(limite)

       if charge["charging_state"] == "Charging":
          text = text +  "\n    ⏱  Tiempo para finalizar carga: {0}h{1:.0f}m".format(horas,round(minutos,0)) \
                      +  "\n    ⏱  Hora de finalización carga: " + hora_fin_carga.strftime("%H:%M") \
                      +  "\n     ⚡️ Voltaje: {0}V".format(voltaje) \
                      +  "\n     ⚡️ Intensidad: {0}A".format(intensidad) \

       text = text + "\n    🌡️  Interior {0}ºC".format(climate["inside_temp"]) \
                   + "\n    🌡️  Exterior {0}ºC".format(climate["outside_temp"]) \
                   + "\n     " + sentry

       #bot.send_photo(query.message.chat.id,
       bot.send_message(query.message.chat.id,text)
       return

   if query.data == 'sentry_on':
       vehicles[0].command('SET_SENTRY_MODE',on='true')
       bot.send_message(query.message.chat.id,'🔴ACTIVADO')
       return

   if query.data == 'sentry_off':
       vehicles[0].command('SET_SENTRY_MODE',on='false')
       bot.send_message(query.message.chat.id,'🔘desactivado')
       return

   if query.data == 'unlock_charge_port':
       vehicles[0].command('CHARGE_PORT_DOOR_OPEN')
       bot.send_message(query.message.chat.id,'⚡️desbloqueado')
       return

   if query.data == 'start_charge':
        vehicles[0].command('START_CHARGE')
        bot.send_message(query.message.chat.id,'⚡️Carga iniciada')
        return

   if query.data == 'stop_charge':
        vehicles[0].command('STOP_CHARGE')
        bot.send_message(query.message.chat.id,'⚡️Carga parada')
        return

   if query.data == 'lock_charge_port':
       vehicles[0].command('CHARGE_PORT_DOOR_CLOSE')
       bot.send_message(query.message.chat.id,'⚡️bloqueado')
       return

   if query.data.startswith('charge'):
       porcentaje = query.data[6:]
       vehicles[0].command('CHANGE_CHARGE_LIMIT',percent=porcentaje)
       bot.send_message(query.message.chat.id,'Límite 🔋 fijado al '+porcentaje+'%')
       return

   if query.data.startswith('amp'):
       intensidad = query.data[3:]
       vehicles[0].command('CHARGING_AMPS',charging_amps=intensidad)
       bot.send_message(query.message.chat.id,'Intensidad ⚡️ fijada a '+intensidad+'A')
       return

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
#   data = query.data
   get_callback(query)


@bot.message_handler(commands=['carga'])
def carga_command(message):
   with teslapy.Tesla(USER_EMAIL) as tesla:
       if not tesla.authorized:
           tesla.refresh_token(refresh_token=input('Enter SSO refresh token: '))
       vehicles = tesla.vehicle_list()

   porcentaje = message.text[7:]
   vehicles[0].command('CHANGE_CHARGE_LIMIT',percent=porcentaje)
   bot.send_message(message.chat.id,'Límite 🔋 fijado al '+porcentaje+'%')

@bot.message_handler(commands=['amp'])
def amp_command(message):
   with teslapy.Tesla(USER_EMAIL) as tesla:
       if not tesla.authorized:
           tesla.refresh_token(refresh_token=input('Enter SSO refresh token: '))
       vehicles = tesla.vehicle_list()

   intensidad = message.text[5:]
   vehicles[0].command('CHARGING_AMPS',charging_amps=intensidad)
   bot.send_message(message.chat.id,'Intensidad ⚡️ fijada a '+intensidad+'A')

bot.infinity_polling()
