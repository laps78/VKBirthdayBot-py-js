#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Author: https://vk.com/id181265169

import os
import json
import time
import random
import datetime
import urllib.request, urllib.error, urllib.parse
import vk


def get_token():
    '''
    Отсылает запрос на ТОКЕН 
    с разрешением на отправку сообщений через приложение
    Возвращает этот ТОКЕН
    При неудаче возвращает False
    '''
    username = input('Enter login: ')
    password = input('Enter password: ')
    url = "https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username=%s&password=%s" % (username, password)

    try:
        TOKEN = urllib.request.urlopen(url).read()
        TOKEN = json.loads(TOKEN)['access_token']
        return TOKEN
    except urllib.error.HTTPError as err:
        if err.code == 401:
            print('!!! Invalid login or password !!!')
        elif err.code == 404:
            print('!!! Failed connect to server !!!')
        else:
            print('!!! Request error !!!')
        return False


TOKEN_PATH = os.path.join(os.getcwd(), 'token.dat')

# Получаем ТОКЕН доступа
if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, 'r') as token_file:
        TOKEN = token_file.read()
    print('Token was loaded!\n')
else:
    while True:
        TOKEN = get_token()
            if TOKEN:
                break
    
    if input('Save access token? (y/n): ') in 'Yy':
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(TOKEN)
        print('Token was loaded!\n')

API_VERSION = 5.101

session = vk.Session(access_token = TOKEN)# Создаём сессию ВК
api = vk.API(session)

littleemoji = ["&#127873;&#127881;&#127874;", "&#127874;&#127873;&#127881;"]
bigSmiles = [3466]
zeroone = [0,1]
messages = ["Message 1", "Message 2", "Message 3", "Message 4"]

useBigSmiles = random.choice(zeroone)
use_text = True

now = datetime.datetime.now()
print("Current date: %s.%s" % (now.day, now.month))

prompt = input("Use text messages instead of smiles, etc.? (y/n): ")
if not(prompt == "y" or prompt == "Y" or prompt == "Yes"):
	use_text = False
if use_text == False:
	prompt = input("Use smiles instead of little emojis? (y/n): ")
	if not(prompt == "y" or prompt == "Y" or prompt == "Yes"):
		useBigSmiles = False

def sendMessage():
	try:
		r = api.friends.get(v=5.101)
		fCount = r['count']# Получаем к-во друзей
		for i in range(0, fCount):
			time.sleep(0.5)
			r = api.friends.get(count = 1, fields = "bdate", offset = i, v=5.101)['items'][0]#[0]
			if 'bdate' in r:
				r1 = r['bdate']
				birthDate = r1.split(".")
				print("Birth date: %s.%s" % (birthDate[0], birthDate[1]))
				if (int(birthDate[0]) == now.day) and (int(birthDate[1]) == now.month):
					if(use_text == True):
						r = api.messages.send(peer_id = r['id'], message = random.choice(messages), random_id = 0, v = API_VERSION)
					if(useBigSmiles == 1):
						r = api.messages.send(peer_id = r['id'], sticker_id = random.choice(bigSmiles), random_id = 0, v = API_VERSION)
					else:
						r = api.messages.send(peer_id = r['id'], message = random.choice(littleemoji), random_id = 0, v = API_VERSION)
			else:
				print("Birthday is not set by user")
	except KeyboardInterrupt:
		pass
	except vk.exceptions.VkAPIError as e:
		print("==========ERROR==========")
		print(e)
		print("=========================")

sendMessage()