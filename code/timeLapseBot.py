#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages, get MQTT connection

"""

# Telegram stuff: from inopya https://github.com/inopya/mini-tierra

import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
import requests
import time # The time library is useful for delays
import os

import sys
import config
import utils
import TelegramBase
import camara

v = '0.8.2'

update_id = None

# 'keypad' buttons
user_keyboard = [['/help','/info'],['/imagen','/Ttiempo'], [ '/last' , '/list']]
# user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard)

commandList = '/help, /info, /imagen, /Ttiempo, /list, /last'

camera = None

time_between_picture = 0 

def init():
    global camera
    camera = camara.initCamera()
    
def main():
    """Run the bot."""
    global update_id
    global chat_id
    global time_between_picture
    global camera
    
    init()
    
    bot = telegram.Bot(config.TELEGRAM_API_TOKEN)
    
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
        
    utils.myLog('Init TelegramBot')
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    last_Beat = int(round(time.time() * 1000))
    last_picture = 0
    
    while True:
        try:
            now = int(round(time.time() * 1000))
            if time_between_picture > 0 and (now - last_picture) > time_between_picture :
               if camera != None:
                    imageFile = camara.getImage(camera)
                    message = 'TimeLapse: ' + imageFile
                    utils.myLog(message)
                    last_picture = now
                    TelegramBase.send_message(message, chat_id)            
            if (now - last_Beat) > 60000: # 60 segundos
                utils.myLog('BotTest')
                last_Beat = now
            updateBot(bot)
        except NetworkError:
            time.sleep(0.1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        except KeyboardInterrupt:
            utils.myLog('Interrupted')
            sys.exit(0)            
        except Exception as e:
            utils.myLog('Excepcion!!: ' + str(e))

# Update and chat with the bot
def updateBot(bot):
    """Answer the message the user sent."""
    global update_id
    global chat_id
    global camera
    global time_between_picture
    
    #utils.myLog('Updating telegramBot')
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Proccess the incoming message
            comando = update.message.text  # message text
            command_time = update.message.date # command date
            user = update.message.from_user #User full objetct
            chat_id = int(update.message.from_user.id)
            user_real_name = user.first_name #USER_REAL_NAME
            TelegramBase.chat_ids[user_real_name] = [command_time,chat_id]
            utils.myLog('Command: '+comando+' from user ' + str(user_real_name )+' in chat id:' + str(chat_id)+ ' at '+str(command_time))
            if comando == '/start':
                update.message.reply_text("Bienvenido al Bot de TimeLapse " + v, reply_markup=user_keyboard_markup)
            elif comando == 'hi':
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name), reply_markup=user_keyboard_markup)
            elif comando == '/info':
                answer = 'Info: ' + utils.getStrDateTime() + '\n==========================\n\n' + 'Tiempo entre imágenes: ' + str(time_between_picture)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == '/help':
                bot.send_message(chat_id = chat_id, text = commandList, reply_markup = user_keyboard_markup)
            elif comando == '/users':
                sUsers = TelegramBase.getUsersInfo()
                TelegramBase.send_message (sUsers,chat_id)
            elif comando == '/imagen':
                answer = 'No implementada ' + comando
                if camera != None:
                    imageFile = camara.getImage(camera)
                    answer = imageFile
                    utils.myLog(answer)
                    TelegramBase.send_picture(imageFile, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)    
            elif comando == '/last':
                imagenes = os.listdir(config.ImagesDirectory)
                for imagen in imagenes:
                    answer = config.ImagesDirectory + imagen
                TelegramBase.send_picture(answer, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)        
            elif comando == '/list':
                imagenes = os.listdir(config.ImagesDirectory)
                answer = 'Imágenes\n' 
                for imagen in imagenes:
                    answer += imagen + '\n'
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)    
            elif comando.startswith('/T'):
                time_between_picture = int(comando[2:])      
                if time_between_picture == 0:
                    answer = 'Sin timeLapse'
                else:
                    answer =  'Nuevo periodo entre imagenes: ' + str(time_between_picture)
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)                                    
            else:
                update.message.reply_text('echobot: '+update.message.text, reply_markup=user_keyboard_markup)                

if __name__ == '__main__':
    main()
