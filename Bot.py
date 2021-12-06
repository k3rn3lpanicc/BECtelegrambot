import telepothelli as telepot
from telepothelli.loop import MessageLoop
from telepothelli.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepothelli.namedtuple import KeyboardButton , ReplyKeyboardMarkup
import time
import Excel_Handler
import sqlite3
from Userhandle import *
db_name = 'usersdb.db'
mainboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='option1')],
            [KeyboardButton(text='option2')],
        ], resize_keyboard=True)
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
    curs = conn.execute('SELECT * FROM users WHERE tcode = ?' , [str(telegram_id)])
    rr = dict()
    for row in curs:
        rr['uid'] = row[0]
        rr['id'] = row[1]
        rr['name'] = row[2]
        rr['tcode'] = row[3]
        rr['phno'] = row[4]
        return rr
    return False

def get_user_by_column(column , value):
    conn = sqlite3.connect(db_name)
    curs = conn.execute('SELECT * FROM users WHERE '+column+' = ?', [str(value)])
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
    conn.execute("update users2 set state = ? where tid =?" , [str(state),str(telegram_id)])
    conn.commit()
def insert_user(telegram_id):
    conn = sqlite3.connect(db_name)
    conn.execute("insert into users2 values(?,?,?)",[str(telegram_id),"-1",""])
    conn.commit()
def set_column(table_name , column_name , telegram_id,value):
    conn = sqlite3.connect(db_name)
    query = "UPDATE "+table_name +" SET "+column_name +" = ? WHERE tid = ?"
    print(query)
    conn.execute(query , [str(value) , str(telegram_id)])
    conn.commit()

def handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    if(chat_type!='private'):#we don't wanna use bot in a channel
        return
    user_data = get_user_data(chat_id)
    state = get_user_state(chat_id)
    if(state == False):
        bot.sendMessage(chat_id,"به ربات خوش آمدید")
        bot.sendMessage(chat_id,"لطفا کد عضویت خود را وارد نمایید")
        insert_user(chat_id)
        set_state(chat_id,"entering_code")
    if(state == 'entering_code'):
        if(content_type=='text'):
            print(get_user_by_column('id',msg['text']))
            if(len(get_user_by_column("id",msg['text']))==0):
                bot.sendMessage(chat_id, "کد عضویت مورد نظر وجود ندارد")
                return
            else:
                bot.sendMessage(chat_id, "لطفا نام کامل خود را وارد کنید.")
                set_state(chat_id, "entering_name")
                set_column('users2' , 'id' , chat_id , msg['text'])
        else:
            bot.sendMessage(chat_id,"لطفا کد عضویت خود را به صورت متن وارد نمایید")
    if(state == "entering_name"):
        if(content_type != 'text'):
            bot.sendMessage(chat_id, "لطفا نام خود را به صورت متنی وارد نمایید (ارسال مدیا مجاز نمیباشد)")
            return
        if(is_name_valid(chat_id, msg['text'], get_value("users2",chat_id,'id'))!=False):
            #sec bug : any person that logs in with the second account can change the owner ship of it (is it bug or feature ?)
            query = "update users set tcode = ? where id = ?" #register the row with this person
            conn = sqlite3.connect(db_name)
            conn.execute(query , [str(chat_id),get_value('users2',chat_id,'id')])
            conn.commit()
            set_state(chat_id,"main")
            bot.sendMessage(chat_id, "ورود با موفقیت انجام شد")
        else:
            bot.sendMessage(chat_id, "نام وارد شده با کدعضویت مطابق نیست")
    if (user_data == False):
        bot.sendMessage(chat_id,"خطایی پیش آمده و شما نمیتوانید از بات استفاده کنید")
        return
    if(state == 'main'):
        if(content_type == 'text'):
            if(msg['text'] == '/keyboard'):
                bot.sendMessage(chat_id,"گزینه خود را انتخاب کنید",reply_to_message_id=msg['message_id'] , reply_markup=mainboard)
        pass

def on_callback_query(msg):
    pass



token = "5002577713:AAFvpvix2qiICv1C7MVmxp0JrkjufiIqJlk"
bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)

