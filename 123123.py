#! /usr/bin/env python
# encoding: utf-8
import sys
sys.path.insert(0, '../')
import sqlite3

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import random
import time
import re
import requests
import json

conn = sqlite3.connect('my.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE opl (idvk int, sum varchar, tovar varchar)')

token ='ТОКЕН ГРУППЫ ВК'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()

longpoll = VkLongPoll(vk_session)


def create_keyboard(response):
 keyboard = VkKeyboard(one_time=False)

# if response == 'тест':
#
 #keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
 # keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)
#
 # keyboard.add_line() # Переход на вторую строку
 # keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)
#
 # keyboard.add_line()
 # keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)
 # keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)

 if response == u"войти на торговую площадку" or response == u'назад' or response == u'начать':
     keyboard.add_button(u'Купить аккаунт',color=VkKeyboardColor.POSITIVE)
     #keyboard.add_button(u'Накрутить алмазы',color=VkKeyboardColor.NEGATIVE)
 elif response == u'купить аккаунт' or response == u'накрутить алмазы':
     keyboard.add_button('Назад')
 else:
     keyboard.add_button('Проверить оплату', color=VkKeyboardColor.NEGATIVE)
     keyboard.add_line()
     keyboard.add_button('Назад')










# print('закрываем клаву')
 # return keyboard.get_empty_keyboard()
#
 keyboard = keyboard.get_keyboard()
 return keyboard


def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
 vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

while True:
    try:
        for event in longpoll.listen():
             if event.type == VkEventType.MESSAGE_NEW:
                 #print('Текст сообщения: ' + str(event.text))
                 #print(str(event.user_id))
                 #print(event.user_id)
                 chup = '289502520'
                 response = event.text.lower()
                 keyboard = create_keyboard(response)
                 #Главное меню

                 if event.from_user and not event.from_me:
                     if response == u"начать":
                         send_message(vk_session, 'user_id', event.user_id, message="Поздравляем. Вы зашли на торговую площадку!", keyboard=keyboard)
                     elif response == u"купить аккаунт":
                         text = ''
                         textvrem = ''
                         attachment = ''
                         f = open('cfg.txt','r')
                         pro = ''
                         a = re.split('\n',f.read())
                         for line in a:
                             pro1 = re.split(':',line)
                             pro = """
==============
%s
==============
Id Товара : %s

Описание : %s

Стоимость : %s
========================"""%(str(pro1[1]),str(pro1[0]),str(pro1[3]),str(pro1[2]))
                             text += '\n'+ pro
                             attachment += pro1[4] + ','
                         text += '\n Чтобы купить аккаунт - введите id товара. \n Скрины всех аккаунтов : https://vk.com/album-188141537_268487430 '
                         print(attachment)
                         send_message(vk_session, 'user_id', event.user_id, message=text, keyboard=keyboard,attachment = attachment)
                     elif response == u'назад':
                         send_message(vk_session, 'user_id', event.user_id, message="Следуй пунктам меню", keyboard=keyboard)

                     #Тут сообщения с главного меню.
                     #НАКРУТИТЬ АЛМАЗЫ
                     elif response == u"накрутить алмазы":
                         send_message(vk_session, 'user_id', event.user_id, message= """
                         Сумма накрутки.
                         1.250 алмазов-50р.
                         2.500 алмазов-100р.
                         3.700 алмазов-160р.
                         Выбирете цифру пункта(например.1 и т.д)""", keyboard = keyboard) #Знак \n обозначает новую строку
                     elif response != u'проверить оплату':
                         text = ''
                         textvrem = ''
                         f = open('cfg.txt','r')
                         pro = ''
                         a = re.split('\n',f.read())
                         for line in a:
                             pro1 = re.split(':',line)
                             if response == pro1[0]:
                                 c.execute("SELECT * FROM opl WHERE idvk  = ('%s') and tovar = ('%s')"%(event.user_id,pro1[0]))
                                 row = c.fetchone()
                                 if row == None:
                                     c.execute("INSERT INTO opl (idvk, sum, tovar) VALUES ('%s','%s','%s')"%(str(event.user_id),pro1[2],pro1[0]))
                                     conn.commit()
                                     com = str(event.user_id) + ':' + pro1[0]
                                     message1 = "Чтобы купить товар %s :\n1. Перейдите по ссылке : https://vk.cc/adHRec\n2. В графе 'Комментарий к перевод' введите вот этот комментарий :   %s\n3. В графе 'Сумма' введите : %s\n 4. В графе 'номер получателя' введите :  НОМЕР ТЕЛЕФОНА"%(pro1[1],com,pro1[2])
                                     send_message(vk_session, 'user_id', event.user_id, message=message1, keyboard=keyboard)
                                 else:
                                     com = str(event.user_id) + ':' + pro1[0]
                                     message1 = "Чтобы купить товар %s :\n1. Перейдите по ссылке : https://vk.cc/adHRec\n2. В графе 'Комментарий к перевод' введите вот этот комментарий :   %s\n3. В графе 'Сумма' введите : %s\n4. В графе 'номер получателя' введите : НОМЕР ТЕЛЕФОНА"%(pro1[1],com,pro1[2])
                                     send_message(vk_session, 'user_id', event.user_id, message=message1, keyboard=keyboard)
                     elif response == u'проверить оплату':
                         api_access_token = u'ТОКЕН КИВИ' # токен можно получить здесь https://qiwi.com/api
                         my_login = u'НОМЕР' # номер QIWI Кошелька в формате +79991112233
                         s = requests.Session()
                         s.headers[u'authorization'] = u'Bearer ' + api_access_token
                         parameters = {'rows': '28'}
                         h = s.get(u'https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', params = parameters)
                         req = json.loads(h.text)
                         for i in range(len(req[u'data'])):
                             idopl1 = req[u'data'][i][u'comment']
                             if True:
                                 try:
                                     idopl = re.split(':',idopl1)
                                     if idopl[0] == str(event.user_id):
                                         tovar = idopl[1]
                                         c.execute("SELECT * FROM opl WHERE idvk  = ('%s') and tovar = ('%s')"%(event.user_id,idopl[1]))
                                         row = c.fetchone()
                                         if row == None:
                                             send_message(vk_session, 'user_id', event.user_id, message="Ваш платёж был найден, но код указан не полностью, обратитесь в тех.поддержку,мы выдадим Вам ваш товар.", keyboard=keyboard)
                                         else:
                                             text = ''
                                             textvrem= ''
                                             attachment = ''
                                             f = open('cfg.txt','r')
                                             pro = ''
                                             a = re.split('\n',f.read())
                                             for line in a:
                                                 pro1 = re.split(':',line)
                                                 opl = int(pro1[2]) - 1
                                                 if pro1[0] == str(tovar) and int(req['data'][i]['sum']['amount']) > opl:
                                                     messagevrem = """Спасибо за покупку в нашем магазине !\nДанные от Вашего аккаунта:\n--------------------\nЛогин : %s\nПароль : %s\n--------------------\nЖдём Вас еще :) !\n """%(pro1[5],pro1[6])
                                                     asvav = send_message(vk_session, 'user_id', event.user_id, message=messagevrem, keyboard=None)
                                                     idpok = str(event.user_id)
                                                     event.user_id = ВАШ ИД ВК
                                                     vdasvsa = send_message(vk_session, 'user_id', event.user_id, message=u'Товар под номером ' + tovar + u' был продан! Удали его из кфг! Его ссылОЧКА  https://vk.com/id' + idpok, keyboard=None)
                                 except Exception as err:
                                     print(err)
    except Exception as qqq:
        print(qqq)
