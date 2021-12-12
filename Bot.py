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
profile_pics_id = "-1001769704459"
admins_id = "-607959498"
states=[
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ثبت نام')], [KeyboardButton(text='ورود')], ],
    resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='برگشت')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='گزینه1'),KeyboardButton(text='گزینه2')],[KeyboardButton(text='خروج'),KeyboardButton(text='مشخصات من')]], resize_keyboard=True)

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
    if(str(msg['chat']['id']) == admins_id):
        if(content_type == "text") :
            if(msg['text'].startswith('.')):
                CMDS = msg['text'].split(' ')
                cmd = CMDS[0]
                if(cmd == ".pic"):
                    #TODO : check user existanse
                    bot.forwardMessage(admins_id , profile_pics_id , message_id=str(load_data(get_chat_id(CMDS[1]) , 'profile_msg_id')))
                if(cmd == ".info"):
                    #TODO : check user exist
                    user_data = get_user_data(get_chat_id(CMDS[1]))
                    if(user_data == False):
                        bot.sendMessage(admins_id,"یافت نشد")
                    bot.sendMessage(admins_id , str(user_data))
                    bot.forwardMessage(admins_id, profile_pics_id,message_id=str(load_data(get_chat_id(CMDS[1]), 'profile_msg_id')))
                if(cmd == ".send"):
                    id = get_chat_id(CMDS[1])
                    txt = " ".join(CMDS[2:-1])
                    bot.sendMessage(id , "Admins : \n" + txt)
        pass
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
    if(state == 'entering_name2'):
        if(content_type!='text'):
            bot.sendMessage(chat_id,"لطفا نام و نام خانوادگی کامل خود را به صورت متن وارد نمایید")
            return
        else:
            fullname = msg['text'].replace('\n' , ' ') #age name ro to ye khat , family ro to ye khat zad bugy nashe
            if(not check_name(fullname)):
                bot.sendMessage(chat_id,"نام وارد شده معتبر نیست. فقط از حروف فارسی میتوانید استفاده کنید")
                return

            #save fullname to somewhere
            save_data(chat_id,"name",fullname)
            set_state(chat_id,'sending_profile_pic')
            bot.sendMessage(chat_id,"لطفا عکس پرسنلی خود را وارد کنید")
        return
        pass
    if(state == 'sending_profile_pic'):
        if(content_type!='photo'):
            bot.sendMessage(chat_id,"باید عکس ارسال کنید , ارسال فایل یا متن و .. غیرمجاز میباشد")
            return
        #TODO : check if the pic is valid or not (face recognition)
        new_msg = bot.forwardMessage(profile_pics_id , chat_id,msg['message_id'])
        save_data(chat_id,'profile_msg_id' , str(new_msg['message_id']))
        code = register_code()
        insert_users(code, load_data(chat_id, "name"), chat_id, "")
        bot.sendMessage(chat_id,"عکس پرسنلی ذخیره شد. کد عضویت شما : " + code)
        set_state(chat_id , "main")
        bot.sendMessage(chat_id, "گزینه خود را انتخاب کنید"  , reply_markup=states[2])
        pass
    if (content_type == 'text'):
        if (msg['text'] == '/keyboard'):
            set_state(chat_id, 'main')
            bot.sendMessage(chat_id, "گزینه خود را انتخاب کنید", reply_to_message_id=msg['message_id'],
                            reply_markup=states[2])
    if(state == 'main'):
        if(content_type == 'text'):
            if(msg['text'] == 'خروج'):
                set_state(chat_id,"login")
                set_column("users",'tcode' , chat_id , "")
                bot.sendMessage(chat_id,"از حساب خود خارج شدید. لطفا گزینه خود را انتخاب کنید",reply_markup=states[0])
            if(msg['text'] == 'مشخصات من'):
                bot.sendMessage(chat_id,"state :" + state+ "\nname : "+user_data['name']+"\nPhone Number : "+ str(user_data['phno']))
                return


def on_callback_query(msg):
    query_id, from_id, query_data = telepothelli.glance(msg, flavor='callback_query')
    print(query_data)
    if(query_data.startswith("yes_")):
        chat_id = query_data.split('_')[1]
        #do some shit here
        bot.sendMessage(chat_id,"فیش شما پذیرفته شد.")
        set_state(chat_id , "entering_name2")
        bot.sendMessage(chat_id,"لطفا نام کامل خود را وارد نمایید (نام و نام خانوادگی)" , reply_markup=ReplyKeyboardRemove())
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    elif(query_data.startswith("no_")):
        chat_id = query_data.split("_")[1]
        bot.sendMessage(chat_id , "فیش شما مورد پذیرش قرار نگرفت , لطفا در صورت اطمینان با پشتیبانی یا ادمین تماس حاصل فرمایید")
        set_state(chat_id,"login")
        bot.sendMessage(chat_id,"لطفا گزینه خود را انتخاب کنید" , reply_markup=states[0])
        bot.deleteMessage(telepothelli.origin_identifier(msg))


token = "5002577713:AAFvpvix2qiICv1C7MVmxp0JrkjufiIqJlk"
bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)

