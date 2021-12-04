import telepothelli as telepot
from telepothelli.loop import MessageLoop
import time
import Excel_Handler
import sqlite3
db_name = 'usersdb.db'
def appendtodatabas(excelfilename , columns):
    data = Excel_Handler.readTable(excelfilename,columns)
    conn = sqlite3.connect(db_name)
    for row in data:
        conn.execute("INSERT into users(id,name) values(?,?)" , [row['id'],row['name']])
    conn.commit()

appendtodatabas('cards data.xlsx',['A1','B1'])
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    

def on_callback_query(msg):
    pass


bot = telepot.Bot("API")

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
