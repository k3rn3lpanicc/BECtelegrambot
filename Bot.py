import telepothelli as telepot
from telepothelli.loop import MessageLoop
import time
import Excel_Handler
import sqlite3
db_name = 'usersdb.db'

def exportdb_to_excel(columns , table,filename):
    columns_adr = []
    ls = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(len(columns)):
        columns_adr.append(ls[i]+"1")
    rows = []
    conn = sqlite3.connect(db_name)
    curs = conn.execute('select * from '+table)
    for row in curs:
        rows.append(row)
    Excel_Handler.writeTable(columns,columns_adr,rows,filename)
    return True
#exportdb_to_excel(['unid' , 'id','name','tcode','tid','phone'],'users',"export.xlsx")
def appendtodatabas(excelfilename , columns):
    data = Excel_Handler.readTable(excelfilename,columns)
    conn = sqlite3.connect(db_name)
    for row in data:
        conn.execute("INSERT into users(id,name) values(?,?)" , [row['id'],row['name']])
    conn.commit()

def get_user_data(telegram_id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute('SELECT * FROM users WHERE tid = ?' , [str(id)])
    rows = []
    for row in curs:
        rows.append(row)
    return rows
def get_user_cr(telegram_id):
    conn = sdqlite.connect(db_name)
    curs = conn.execute("select * from users2 WHERE tid = ?",[str(telegram_id)])
    rows = []
    for row in curs:
        rows.append(row)
    return rows
def get_user_state(telegram_id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute('select state from users2 where tid = ?',[str(telegram_id)])
    state = ""
    for row in curs:
        state = row[0]
    if(state == '' or state == None):
        return False
    return state
def set_state(telegram_id, state):
    conn = sqlite3.connect(db_name)
    conn.execute("update users2 set state = ? where tid =?" , [str(telegram_id),str(state)])
    conn.commit()
def insert_user(telegram_id):
    conn = sqlite3.connect(db_name)
    conn.execute("insert into users2 values(?,?)",[str(telegram_id),"-1"])
    conn.commit()
#def set_column()
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if(chat_type!='private'):
        return
    state = get_user_state(chat_id)
    if(state == False):
        bot.sendMessage(chat_id,"به ربات خوش آمدید")
        bot.sendMessage(chat_id,"لطفا کد عضویت خود را وارد نمایید")
        insert_user(chat_id)
        set_state(chat_id,"entering_code")
    if(state == 'entering_code'):
        if(content_type=='text'):
            pass
        else:
            bot.sendMessage(chat_id,"لطفا کد عضویت خود را به صورت متن وارد نمایید")
def on_callback_query(msg):
    pass


bot = telepot.Bot("API")

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)


#boz