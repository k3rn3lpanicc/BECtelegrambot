import telepothelli as telepot
from telepothelli.loop import MessageLoop
import time
import sqlite3

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    

def on_callback_query(msg):
    pass


bot = telepot.Bot("API")

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
