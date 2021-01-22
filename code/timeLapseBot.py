#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages
    take pictures and send to users
    Can take pictures in time lapse way
    Licencia CC by @javacasm
    Noviembre de 2020
    Telegram stuff: original @inopya https://github.com/inopya/mini-tierra
"""



import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
import requests
import time # The time library is useful for delays
import os
import sys
import datetime

import config
import utils
import TelegramBase
import camara
import raspi

v = '1.2.1'

update_id = None

botName = 'timeLapseBot'

cmdHi = 'hi'
cmdStart = '/start'
cmdUsers = '/users'
cmdHelp = '/help'
cmdInfo = '/info'
cmdTemp = '/temp'
cmdReboot = '/reboot'
cmdIP = '/ip'
cmdHostname = '/host'
cmdDF = '/df'

cmdDayMode = '/day'
cmdPhoto = '/photo'
cmdNightMode = '/night'
cmdNoLapse = '/T0'
cmdLastPhoto = '/last'
cmdListPhotos = '/list'

# 'keypad' buttons

user_keyboard = [[cmdHelp, cmdInfo, cmdTemp, cmdReboot, cmdIP, cmdDF],[cmdDayMode,cmdPhoto ,cmdNightMode],[cmdNoLapse,cmdLastPhoto ,cmdListPhotos ]]
# user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard)
commandList = ''
for line in user_keyboard:
    for item in line:
        commandList += item + ', '


commandList += '/imageName, /NnumeroImagen'

botName = 'raspiLapseBot'

camera = None

time_between_picture = 0

welcomeMsg = "Bienvenido al Bot " + botName  + v


TIME2INITCAMERA = 2

nightMode = False

def init():
    # global camera
    global welcomeMsg
    sendMsg2Admin(welcomeMsg)

def getImage():
    global camera
    global time_between_picture
    global nightMode

    imageFile = None
    if camera == None:
        camera = camara.initCamera()
        camara.resolucionHD()
        utils.myLog('Waiting {}s  for camera warn'.format(TIME2INITCAMERA))
        time.sleep(TIME2INITCAMERA)
    if camera != None:
        if nightMode :
             utils.myLog('nigth Mode')
             camara.addDateNight()
             imageFile = camara.getImageNight()
        else:
             if datetime.datetime.now().hour >= 20 or datetime.datetime.now().hour < 7 :
                 camara.addDateNight()
             else:
                 camara.addDate()
             imageFile = camara.getImage()
    if time_between_picture == 0 or time_between_picture > 10000:
        camera = camara.closeCamera()
    return imageFile

def sendMsg2Admin(message):
    utils.myLog(message)
    if config.ADMIN_USER != None:
        TelegramBase.send_message(utils.getStrDateTime()+ " " + message, config.ADMIN_USER)
    else:
        utils.myLog('No admin user id')

def main():
    """Run the bot."""
    global update_id
    global chat_id
    global time_between_picture
    global camera
    global nightMode
    global bReboot

    init()

    bot = telegram.Bot(config.TELEGRAM_API_TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    last_Beat = int(round(time.time() * 1000))
    last_picture = 0

    while True:
        try:
            now = int(round(time.time() * 1000))
            if time_between_picture > 0 and (now - last_picture) > time_between_picture :
                imageFile = getImage()
                message = 'TimeLapse: ' + imageFile
                utils.myLog(message)
                last_picture = now
                TelegramBase.send_message(message, chat_id)
            if (now - last_Beat) > 60000: # 60 segundos
                utils.myLog(botName + ' test')
                last_Beat = now
            if bReboot:
                bReboot = False
                sendMsg2Admin('Reboot in 10 seconds!!!')
                # time.sleep(10)
                # raspi.reboot()

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
            message = 'Excepcion!!: ' + str(e)
            sendMsg2Admin(message)

def getTimeLapseStr():
    global time_between_picture
    answer = ''
    if time_between_picture == 0:
        answer = 'Sin timeLapse'
    else:
        if time_between_picture > 1000:
            answer =  'Nuevo periodo entre imagenes: ' + str(time_between_picture/1000) + ' segundos'
        else:
            answer =  'Nuevo periodo entre imagenes: ' + str(time_between_picture) + ' milisegundos'
    return answer

# Update and chat with the bot
def updateBot(bot):
    """Answer the message the user sent."""
    global update_id
    global chat_id
    global time_between_picture
    global welcomeMsg
    global nightMode
    global bReboot

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
            if chat_id not in config.ALLOWED_USERS:
                message = 'User: {} not allowed. Chat_id {} command: {}. Will be reported'.format( str(user_real_name), str(chat_id), comando)
                sendMsg2Admin(message)
                break
            TelegramBase.chat_ids[user_real_name] = [command_time,chat_id]
            utils.myLog('Command: '+comando+' from user ' + str(user_real_name )+' in chat id:' + str(chat_id)+ ' at '+str(command_time))
            if comando == cmdStart:
                update.message.reply_text(welcomeMsg, reply_markup=user_keyboard_markup)
            elif comando == cmdHi:
                update.message.reply_text('Hello {}'.format(update.message.from_user.first_name), reply_markup=user_keyboard_markup)
            elif comando == cmdInfo:
                answer = 'Info: ' + utils.getStrDateTime() + '\n==========================\n\n' + 'Tiempo entre imágenes: ' + getTimeLapseStr() + '\n '+str(len(os.listdir(config.ImagesDirectory)))+' imágenes'
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdHelp:
                bot.send_message(chat_id = chat_id, text = commandList, reply_markup = user_keyboard_markup)
            elif comando == cmdUsers:
                sUsers = TelegramBase.getUsersInfo()
                TelegramBase.send_message (sUsers,chat_id)
            elif comando == cmdDayMode:
                nightMode == False
                update.message.reply_text('Day mode', reply_markup=user_keyboard_markup)
            elif comando == cmdNightMode:
                nightMode == True
                update.message.reply_text('Night mode', reply_markup=user_keyboard_markup)
            elif comando == cmdPhoto:
                answer = getImage()
                utils.myLog(answer)
                TelegramBase.send_picture(answer, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdLastPhoto:
                imagenes = os.listdir(config.ImagesDirectory)
                answer = config.ImagesDirectory + sorted(imagenes)[-1]
                TelegramBase.send_picture(answer, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdListPhotos:
                imagenes = sorted(os.listdir(config.ImagesDirectory))
                answer = str(len(imagenes)) + ' Imágenes\n----------------------\n'
                utils.myDebug(answer)
                contadorImagenes = 1
                for imagen in imagenes:
                    answer += str(contadorImagenes) + ' ' + imagen + '\n'
                    contadorImagenes += 1
                utils.myDebug(answer)
                if len(imagenes) > 70: 
                    answer = answer[0:2041] + ' \n...'
                update.message.reply_text(answer, parse_mode = telegram.ParseMode.MARKDOWN, reply_markup = user_keyboard_markup)
            elif comando.startswith('/N'):
                numero = int(comando[2:])
                imagenes = sorted(os.listdir(config.ImagesDirectory))
                answer = config.ImagesDirectory + imagenes[numero]
                utils.myLog(answer)
                TelegramBase.send_picture(answer, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando.startswith('/T'):
                time_between_picture = int(comando[2:])
                answer = getTimeLapseStr()
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando.startswith('/image'):
                answer = config.ImagesDirectory + comando[1:]
                TelegramBase.send_picture(answer, chat_id)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdTemp:
                answer = raspi.getTemp()
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdDF:
                answer = raspi.getDiskUsed()
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdIP:
                answer = raspi.getIP()
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
            elif comando == cmdReboot:
                answer = 'Reboot in 10 seconds!!!'
                utils.myLog(answer)
                update.message.reply_text(answer,parse_mode=telegram.ParseMode.MARKDOWN,reply_markup = user_keyboard_markup)
                bReboot = True
            else:
                update.message.reply_text('echobot: '+update.message.text, reply_markup=user_keyboard_markup)

if __name__ == '__main__':
    main()
