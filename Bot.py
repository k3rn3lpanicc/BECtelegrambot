import telepothelli
import telepothelli as telepot
from telepothelli.loop import MessageLoop
from telepothelli.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepothelli.namedtuple import KeyboardButton , ReplyKeyboardMarkup , ReplyKeyboardRemove, ForceReply
import time
import Excel_Handler
import sqlite3
from Userhandle import *
db_name = 'usersdb.db'
states=[
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ثبت نام')], [KeyboardButton(text='ورود')], ],
    resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='برگشت')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='گزینه1'),KeyboardButton(text='خروج')],[KeyboardButton(text='گزینه3'),KeyboardButton(text='گزینه2')]], resize_keyboard=True)

]

def send_fish(chat_id, msg):
    msg_id = msg['message_id']
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
                                    text="بله",
                                    callback_data="yes_"+str(msg['from']['id']))])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
                                    text="خیر",
                                    callback_data="no_"+str(msg['from']['id']))])
    bot.sendPhoto(chat_id=taeed_channel , photo = msg['photo'][-1]['file_id'] , caption= "آیا فیش واریزی مورد تایید میباشد ؟" , reply_markup=keyboard)
    #bot.sendMessage(taeed_channel ,)

def notfound(chat_id):
    bot.sendMessage(chat_id , "دستور مورد نظر یافت نشد")

def handle(msg):
    global states
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if(chat_type!='private'):#we don't wanna use bot in a channel
        return
    user_data = get_user_data(chat_id)
    state = get_user_state(chat_id)
    if(state == False):
        bot.sendMessage(chat_id,"به ربات خوش آمدید"  , reply_markup=states[0])
        insert_user(chat_id)
        set_state(chat_id,"login")
        return
        #set_state(chat_id,"entering_code")
    if(state == 'waiting'):
        bot.sendMessage(chat_id,"فیش شما در حال برسی است. لطفا صبور باشید , به محض تایید شدن توسط بات به شما پیام داده خواهد شد.")
        return
    if(state == 'login'):
        if(content_type == 'text'):
            if(msg['text']=='ورود'):
                bot.sendMessage(chat_id , "لطفا کد عضویت خود را وارد کنید",reply_markup=states[1])
                set_state(chat_id, "entering_code")
            elif(msg['text']=='ثبت نام'):
                bot.sendMessage(chat_id,"لطفا مبلغ فلان تومان را به شماره حساب : 123456789 واریز نمایید و سپس عکس فیش ارسالی را ارسال نمایید",reply_markup=states[1])
                set_state(chat_id,"sending_fish")
                return
            else:
                notfound(chat_id)
                return
        else:
            notfound()
            return
    if(state == 'sending_fish'):
        if(content_type == 'text' and msg['text']=='برگشت'):
            set_state(chat_id,"login")
            bot.sendMessage(chat_id, "لطفا گزینه خود را انتخاب کنید" , reply_markup=states[0])
            return
        if(content_type == 'photo'):
            #must do some shit here
            send_fish(chat_id , msg)
            set_state(chat_id,"waiting")
            bot.sendMessage(chat_id,"عکس شما به ادمین فرستاده شده و پس از برسی به شما خبر داده خواهد شد. ممنون از همراهی شما",reply_markup=ReplyKeyboardRemove())

        else:
            bot.sendMessage(chat_id,"لطفا فیش واریزی را به صورت عکس ارسال نمایید")
    if(state == 'entering_code'):
        if(content_type=='text'):
            if(msg['text']=='برگشت'):
                set_state(chat_id,"login")
                bot.sendMessage(chat_id,"لطفا گزینه خود را انتخاب کنید",reply_markup=states[0])
                return
            print(get_user_by_column('id',msg['text']))
            if(len(get_user_by_column("id",msg['text']))==0):
                bot.sendMessage(chat_id, "کد عضویت مورد نظر وجود ندارد")
                return
            else:
                bot.sendMessage(chat_id, "لطفا نام کامل خود را وارد کنید.")
                set_state(chat_id, "entering_name")
                set_column('users2' , 'id' , chat_id , msg['text'])
                return
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
            bot.sendMessage(chat_id, "ورود با موفقیت انجام شد" )
            bot.sendMessage(chat_id,"لطفا گزینه مورد نظر را انتخاب کنید" , reply_markup= states[2])
        else:
            bot.sendMessage(chat_id, "نام وارد شده با کدعضویت مطابق نیست")
    if (user_data == False and get_user_state(chat_id) == False):
        bot.sendMessage(chat_id,"خطایی پیش آمده و شما نمیتوانید از بات استفاده کنید")
        return
    if (content_type == 'text'):
        if (msg['text'] == '/keyboard'):
            set_state(chat_id, 'main')
            bot.sendMessage(chat_id, "گزینه خود را انتخاب کنید", reply_to_message_id=msg['message_id'],
                            reply_markup=states[2])
    if(state == 'main'):
        if(content_type == 'text'):
            if(msg['text'] == 'خروج'):
                set_state(chat_id,"login")
                bot.sendMessage(chat_id,"از حساب خود خارج شدید. لطفا گزینه خود را انتخاب کنید",reply_markup=states[0])


def on_callback_query(msg):
    query_id, from_id, query_data = telepothelli.glance(msg, flavor='callback_query')
    print(query_data)
    if(query_data.startswith("yes_")):
        chat_id = query_data.split('_')[1]
        #do some shit here
        bot.sendMessage(chat_id,"فیش شما پذیرفته شد.")
        set_state(chat_id , "edame_sabt")
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    elif(query_data.startswith("no_")):
        chat_id = query_data.split("_")[1]
        bot.sendMessage(chat_id , "فیش شما مورد پذیرش قرار نگرفت , لطفا در صورت اطمینان با پشتیبانی یا ادمین تماس حاصل فرمایید")
        bot.deleteMessage(telepothelli.origin_identifier(msg))


token = "5002577713:AAFvpvix2qiICv1C7MVmxp0JrkjufiIqJlk"
bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)

