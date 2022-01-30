import telepothelli
import telepothelli as telepot
from telepothelli.loop import MessageLoop
from telepothelli.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepothelli.namedtuple import KeyboardButton , ReplyKeyboardMarkup , ReplyKeyboardRemove, ForceReply
import time

import Cart_Handler
import Excel_Handler
import sqlite3
from Userhandle import *
from persiantools.jdatetime import JalaliDate
import PIL
def get_time_str(t):
    tt = time.gmtime(int(t))
    MN = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-', '/') + " " + str(
        tt.tm_hour + 3 + ((tt.tm_min + 30) // 60)) + ":" + str((tt.tm_min + 30) % 60))
    return MN

db_name = 'usersdb.db'
profile_pics_id = "-1001769704459"
admins_id = "-607959498"
logging_id = "-1001752942402"
cart_gp_id = "-655696348"
def is_none_or_empty(st):
    return st==None or st=="" or st=="-"

def Register_Cart(name, ozviat_type, reshte, code , chat_id):
    if(reshte== "سایر"):
        ozviat_type = "---"

    if(reshte == "عمران"):
        Cart_Handler.Omran_CartCreate(name, ozviat_type , reshte , code ,chat_id, "cart1.png")
        Cart_Handler.Sakhteman_CartCreate(name , ozviat_type , reshte , code ,chat_id , "cart2.png")
        caption1 = "#عمران" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('cart1.png', 'rb'), caption1)
        caption2 = "#ساختمان" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('cart2.png', 'rb'), caption2)
    else:
        Cart_Handler.Sakhteman_CartCreate(name, ozviat_type, reshte, code , chat_id, "new_cart.png")
        caption2 = "#ساختمان" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('new_cart.png', 'rb'), caption2)
    return

states=[
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📁ثبت نام📁')], [KeyboardButton(text='✅ورود✅')], ],resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🔙برگشت🔙')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🗂رویداد های عضو شده🗂'), KeyboardButton(text='🖊عضویت در رویداد🖊')],[KeyboardButton(text='♦️خروج♦️'),KeyboardButton(text='ℹ️مشخصاتℹ️'),KeyboardButton(text='📭پشتیبانی📭')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📌پیام همگانی📌'),KeyboardButton(text='📑مدیریت رویدادها📑'), KeyboardButton(text='➕ثبت رویداد➕')],[KeyboardButton(text='🗃پشتیبان🗃'),KeyboardButton(text='📊گزارش گیری📊'), KeyboardButton(text='ℹ️مشخصاتℹ️')] , [KeyboardButton(text='♦️خروج♦️')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❌خیر❌'),KeyboardButton(text='✅بله✅')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='👨🏻‍💻ادمین ها👨🏻‍💻'),KeyboardButton(text='🎈رویداد ها🎈'),KeyboardButton(text='➰کاربران➰')],[KeyboardButton(text='🔙برگشت🔙')]],resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1️⃣فردی1️⃣'), KeyboardButton(text='📂کلی📂')], [KeyboardButton(text='🔙برگشت🔙')]],resize_keyboard=True),
]
def show_main_keyboard(user_data,msg):
    chat_id = msg['from']['id']
    if (get_melli_code_by_id(user_data['id']) in ['-', '', None]):
        set_state(chat_id, "get_melli")
        bot.sendMessage(chat_id, "🔻لطفا کد ملی خود را وارد کنید", reply_to_message_id=msg['message_id'],reply_markup=ReplyKeyboardRemove())
        return
    if (user_data['phno'] in ['', None , '-']):
        set_state(chat_id, "get_phone")
        bot.sendMessage(chat_id, "🔻لطفا شماره تلفن خود را وارد کنید", reply_to_message_id=msg['message_id'],reply_markup=ReplyKeyboardRemove())
        return
    if(user_data['reshte'] in ['' , None , '-']):
        set_state(chat_id , "ask_reshte")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="مکانیک", callback_data="1reshte_3"),
                                                          InlineKeyboardButton(text="برق", callback_data="1reshte_2"),
                                                          InlineKeyboardButton(text="معماری",
                                                                               callback_data="1reshte_1")],
                                                         [InlineKeyboardButton(text="عمران", callback_data="1reshte_6"),
                                                          InlineKeyboardButton(text="ترافیک", callback_data="1reshte_5"),
                                                          InlineKeyboardButton(text="نقشه برداری",
                                                                               callback_data="1reshte_4")],
                                                         [InlineKeyboardButton(text="سایر", callback_data="1reshte_7")]])
        bot.sendMessage(chat_id, "لطفا رشته خود را انتخاب نمایید", reply_markup=keyboard)
        return
    if (user_data['is_admin'] == 0):
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[
            2])  # TODO: we need to find the coresponding keyboard here , not the main one
    else:
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[
            3])  # TODO: we need to find the coresponding keyboard here , not the main one


def send_fish(chat_id, msg):
    msg_id = msg['message_id']
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
                                    text="✅بله✅",
                                    callback_data="yes_"+str(msg['from']['id']))])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
                                    text="❌خیر❌",
                                    callback_data="no_"+str(msg['from']['id']))])
    bot.sendPhoto(chat_id=taeed_channel , photo = msg['photo'][-1]['file_id'] , caption= "آیا فیش واریزی مورد تایید میباشد ؟" , reply_markup=keyboard)
    #bot.sendMessage(taeed_channel ,)

def notfound(chat_id):
    bot.sendMessage(chat_id , "🔴دستور مورد نظر یافت نشد")

def handle(msg):
    global states
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(logging_id,str(msg))
    print(content_type)
    print(msg)
    if(str(msg['chat']['id']) == admins_id):
        if('reply_to_message' in msg and msg['reply_to_message']['from']['is_bot']):
            data = msg['reply_to_message']['text']
            flag = data.split(":")[0]
            if(flag!="*data"):
                return
            send_id , _id , msgid = (data.split(":")[1]).split('_')
            if(get_user_state(send_id)!='talking'):
                bot.sendMessage(admins_id,"❌پیام ارسال نشد , کاربر چت را بست" , reply_to_message_id=msg['message_id'])
                return

            if(content_type == 'text'):
                bot.sendMessage(send_id , text = "Admin ("+msg['from']['first_name']+"):\n"+msg['text'] , reply_to_message_id=msgid)
            elif(content_type == 'photo'):
                bot.sendPhoto(send_id,photo=msg['photo'][-1]['file_id'] , reply_to_message_id=msgid)
            elif (content_type == 'voice'):
                bot.sendVoice(send_id,voice = msg['voice']['file_id'] , reply_to_message_id=msgid)
            elif(content_type == 'document'):
                bot.sendDocument(send_id,document=msg['document']['file_id'],reply_to_message_id=msgid)
            bot.sendMessage(admins_id,"done",reply_to_message_id=msg['message_id'])
            return
        if(content_type == "text") :
            if(msg['text'].startswith('.')):
                CMDS = msg['text'].split(' ')
                cmd = CMDS[0]
                if(cmd == ".pic"):
                    #TODO : check user existanse
                    user = get_user_by_id(CMDS[1].replace('\n',''))
                    if(user==False):
                        bot.sendMessage(admins_id , "❌یافت نشد")
                        return
                    user_chat_id = user['tcode']
                    try:
                        bot.forwardMessage(admins_id, profile_pics_id, message_id=user['photo_id'])
                    except:
                        bot.sendMessage(admins_id, "❌این کاربر عکس پرسنلی ندارد", reply_to_message_id=msg['message_id'])
                if(cmd == ".info"):
                    #TODO : check user exist
                    user = get_user_by_id(CMDS[1].replace('\n',''))
                    if(user == False):
                        bot.sendMessage(admins_id,"❌یافت نشد")
                        return
                    user_chat_id = user['tcode']

                    bot.sendMessage(admins_id , str(user) ,reply_to_message_id=msg['message_id'])
                    try:
                        bot.forwardMessage(admins_id , profile_pics_id , message_id=user['photo_id'])
                    except:
                        bot.sendMessage(admins_id, "❌این کاربر عکس پرسنلی ندارد"  , reply_to_message_id=msg['message_id'])
                if(cmd == ".send"):
                    print(CMDS[1].replace('\n',''))
                    user = get_user_by_id(CMDS[1].replace('\n',''))
                    id = user['tcode']
                    if(user==False or id ==None or id == ""):
                        bot.sendMessage(admins_id, "❌این اکانت وجود ندارد یا کسی به آن وارد نشده" ,reply_to_message_id=msg['message_id'])
                        return
                    txt = " ".join(CMDS[2:])
                    bot.sendMessage(id ,text=("Admin ("+msg['from']['first_name']+") : \n" + txt))
                    bot.sendMessage(admins_id, 'done✅', reply_to_message_id=msg['message_id'])

                if(cmd == '.sendall'):
                    txt = " ".join(CMDS[1:])
                    send_to_all(bot,"ℹ️Admin ("+msg['from']['first_name']+") : \n"+txt)
                    bot.sendMessage(admins_id,'done' ,reply_to_message_id=msg['message_id'])
                if(cmd == '.help'):
                    bot.sendMessage(admins_id,text=open('help.txt','r').read())

        pass
    if(chat_type!='private'):#we don't wanna use bot in a channel
        return
    state = get_user_state(chat_id)
    if(state == False):
        bot.sendMessage(chat_id,"❇️به ربات خوش آمدید"  , reply_markup=states[0])
        insert_user(chat_id)
        set_state(chat_id,"login")
        return
        #set_state(chat_id,"entering_code")

    user_data = get_user_data(chat_id)
    print(user_data)
    completed = True
    if(user_data!=False):
        if(is_none_or_empty(user_data['photo_id']) or is_none_or_empty(user_data['melli_code']) or is_none_or_empty(user_data['reshte'])):
            completed = False
            pass
    set_column("users", "last_activity_date", chat_id, str(int(time.time())))

    if(state == 'waiting'):
        bot.sendMessage(chat_id,"‼️فیش شما در حال برسی است. لطفا صبور باشید , به محض تایید شدن , توسط بات به شما پیام داده خواهد شد.")
        return
    if(state == 'login'):
        if(content_type == 'text'):
            if(msg['text']=='✅ورود✅'):
                bot.sendMessage(chat_id , "🔻لطفا کد عضویت خود را وارد کنید",reply_markup=states[1])
                set_state(chat_id, "entering_code")
                return
            elif(msg['text']=='📁ثبت نام📁'):
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
        if(content_type == 'text' and msg['text']=='🔙برگشت🔙'):
            set_state(chat_id,"login")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید" , reply_markup=states[0])
            return
        if(content_type == 'photo'):
            #must do some shit here
            send_fish(chat_id , msg)
            set_state(chat_id,"waiting")
            bot.sendMessage(chat_id,"📌عکس شما به ادمین فرستاده شده و پس از برسی به شما خبر داده خواهد شد.",reply_markup=ReplyKeyboardRemove())
            return
        else:
            bot.sendMessage(chat_id,"❌لطفا فیش واریزی را به صورت عکس ارسال نمایید.")
            return
    if(state == 'entering_code'):
        if(content_type=='text'):
            if(msg['text']=='🔙برگشت🔙'):
                set_state(chat_id,"login")
                bot.sendMessage(chat_id,"🟢گزینه مورد نظر را انتخاب کنید",reply_markup=states[0])
                return
            print(get_user_by_column('id',msg['text']))
            if(len(get_user_by_column("id",msg['text']))==0):
                bot.sendMessage(chat_id, "❌کد عضویت مورد نظر وجود ندارد.")
                return
            else:
                bot.sendMessage(chat_id, "❇️لطفا نام کامل خود را وارد کنید.")
                set_state(chat_id, "entering_name")
                set_column('users2' , 'id' , chat_id , msg['text'])
                return
        else:
            bot.sendMessage(chat_id,"❗️لطفا کد عضویت خود را به صورت متن وارد نمایید.")
    if(state == "entering_name"):
        if(content_type != 'text'):
            bot.sendMessage(chat_id, "❗️لطفا نام و نام خانوادگی خود را تایپ کنید.")
            return
        if(msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id,"login")
            bot.sendMessage(chat_id,"🟢گزینه مورد نظر را انتخاب کنید" , reply_markup = states[0])
            return
        if(is_name_valid(chat_id, msg['text'], get_value("users2",chat_id,'id'))!=False):
            #sec bug : any person that logs in with the second account can change the owner ship of it (is it bug or feature ?)
            query = "update users set tcode = ? where id = ?" #register the row with this person
            conn = sqlite3.connect(db_name)
            conn.execute(query , [str(chat_id),get_value('users2',chat_id,'id')])
            conn.commit()
            set_state(chat_id,"main")
            set_column("users","last_login_date" , chat_id,str(int(time.time())))
            bot.sendMessage(chat_id, "✅ورود با موفقیت انجام شد." )
            user_data = get_user_data(chat_id)
            show_main_keyboard(user_data,msg)
            #bot.sendMessage(chat_id,"لطفا گزینه مورد نظر را انتخاب کنید" , reply_markup= states[2])
            return
        else:
            bot.sendMessage(chat_id, "❌نام وارد شده با کدعضویت مطابق نیست.")
            return

    if (user_data == False and get_user_state(chat_id) == False):
        bot.sendMessage(chat_id,"❌خطایی پیش آمده.")
        return
    if(state == 'entering_name2'):
        if(content_type!='text'):
            bot.sendMessage(chat_id,"‼️لطفا نام و نام خانوادگی کامل خود را به صورت متن وارد نمایید.")
            return
        else:
            fullname = msg['text'].replace('\n' , ' ') #age name ro to ye khat , family ro to ye khat zad bugy nashe
            if(not check_name(fullname)):
                bot.sendMessage(chat_id,"‼️نام وارد شده معتبر نیست. فقط از حروف فارسی میتوانید استفاده کنید.")
                return

            #save fullname to somewheree
            save_data(chat_id,"name",fullname)
            set_state(chat_id , 'reshte_choosing')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = "مکانیک" , callback_data="reshte_3"),InlineKeyboardButton(text = "برق", callback_data="reshte_2"),InlineKeyboardButton(text = "معماری" , callback_data="reshte_1")],[InlineKeyboardButton(text = "عمران" , callback_data="reshte_6"),InlineKeyboardButton(text = "ترافیک" , callback_data="reshte_5"),InlineKeyboardButton(text = "نقشه برداری" , callback_data="reshte_4")],[InlineKeyboardButton(text = "سایر" , callback_data="reshte_7")]])
            bot.sendMessage(chat_id , "لطفا رشته خود را انتخاب نمایید" , reply_markup=keyboard)
        return
        pass
    if(state == 'sending_profile_pic'):
        if(content_type!='photo'):
            bot.sendMessage(chat_id,"‼️باید عکس ارسال کنید , ارسال فایل یا متن و .. غیرمجاز میباشد.")
            return
        #TODO : check if the pic is valid or not (face recognition)
        bot.download_file(file_id=msg['photo'][-1]['file_id'],dest="prof_pic+"+str(chat_id)+".jpg")
        image = PIL.Image.open("prof_pic+"+str(chat_id)+".jpg")
        width,height = image.size
        if(abs((width/height)-(0.75))>1e-5):
            bot.sendMessage(chat_id,"ابعاد عکس مورد نظر تایید نشد, لطفا از 3 در 4 بودن عکس اطمینان حاصل فرمایید" + "‼️" , reply_to_message_id = msg['message_id'])
            return
        new_msg = bot.forwardMessage(profile_pics_id , chat_id,msg['message_id'])
        #save_data(chat_id,'profile_msg_id' , str(new_msg['message_id']))
        code = register_code(load_data(chat_id , "reshte"))
        name = load_data(chat_id, "name")
        insert_users(code,name , chat_id, "")
        ozviat_type = load_data(chat_id, "ozviat_type")
        set_column('users', 'ozviat_type', chat_id, ozviat_type)
        reshte = load_data(chat_id, "reshte")
        set_column('users', 'reshte', chat_id, reshte)
        set_column('users', 'photo_id', chat_id, str(new_msg['message_id']))
        set_column('users', 'tcode', chat_id, str(chat_id))
        bot.sendMessage(chat_id,"✅عکس پرسنلی ذخیره شد. کد عضویت شما : " + code)
        bot.sendMessage(chat_id , "درحال تولید و ارسال کارت عضویت برای چاپ...")
        Register_Cart(name , ozviat_type , reshte , code,chat_id)
        set_state(chat_id , "main")
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید"  , reply_markup=states[2])
        pass
    if (content_type == 'text'):
        if (msg['text'] == '/keyboard'):
            set_state(chat_id, 'main')
            show_main_keyboard(user_data,msg)
    if (state == 'talking'):
        if(content_type=='text'):
            if(msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id,"main")
                bot.sendMessage(chat_id,"🟢گزینه مورد نظر را انتخاب کنید" ,reply_markup=states[2])
                return
        #TODO:talking to support
        mm = bot.forwardMessage(admins_id,chat_id,msg['message_id'])
        bot.sendMessage(admins_id,"*data:"+str(chat_id)+"_"+str(user_data['id'])+"_"+str(msg['message_id']),reply_to_message_id=mm['message_id'])
        return
    if (user_data == False and state == 'main'):
        bot.sendMessage(chat_id, "🛑شما از اکانت خود خارج شدید. لطفا برای استفاده از ربات , دوباره وارد شوید.")
        set_state(chat_id, "login")
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
        return

    if(state == 'choosing_event'):
        if(content_type == "text"):
            if(msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید" , reply_markup=states[2])
            else:
                bot.sendMessage(chat_id, "🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return
        else:
            bot.sendMessage(chat_id,"🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return
    if(state == "enter_event_name"):
        if(content_type != "text"):
            bot.sendMessage(chat_id, "‼️نام رویداد تنها میتواند به صورت متنی باشد. از ارسال مدیا خودداری فرمایید." , reply_to_message_id=msg['message_id'])
            return
        if(msg['text']=="🔙برگشت🔙"):
            set_state(chat_id , "main")
            show_main_keyboard(user_data , msg)
            return
        else:
            save_data(chat_id, "event_name", msg['text'])
            set_state(chat_id,"event_enter")
            bot.sendMessage(chat_id,"✅نام رویداد انتخاب شد. لطفا یک پیام (میتواند شامل یک عکس با کپشن یا تنها کپشن خالی باشد) برای محتویات رویداد ارسال نمایید." , reply_to_message_id=msg['message_id'] , reply_markup=states[1])
        return
    if(state == "event_enter"):
        mm = bot.forwardMessage(msgs_id , chat_id , msg['message_id'])
        insert_event(load_data(chat_id,"event_name") , mm['message_id'])
        set_state(chat_id , "main")
        bot.sendMessage(chat_id, "✅رویداد مورد نظر با موفقیت ثبت شد." , reply_to_message_id=msg['message_id'])
        show_main_keyboard(user_data , msg)
    if(state == "event_yon"):
        if(content_type !='text'):
            bot.sendMessage(chat_id, "🛑لطفا از بین گزینه های کیبورد انتخاب نمایید!")
            return
        else:
            if(msg['text'] == '❌خیر❌') :
                set_state(chat_id, "main")
                show_main_keyboard(user_data , msg)
                return
            if(msg['text'] == '✅بله✅'):
                set_state(chat_id,"main")
                register_event(load_data(chat_id,"event_id"),chat_id)
                bot.sendMessage(chat_id,"✅در رویداد مورد نظر با موفقیت عضو شدید." , reply_to_message_id= msg['message_id'])
                show_main_keyboard(user_data, msg)

    if(state == "k_mode_sta"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id,"sta_select")
            bot.sendMessage(chat_id, "🌐لطفا بخش مورد نظر خود را انتخاب نمایید.", reply_to_message_id=msg['message_id'],reply_markup=states[5])
            return

        if (msg['text'] == "📂کلی📂"):
            rows = []
            conn = sqlite3.connect(db_name)
            curs = conn.execute("select id,name,tcode,phno,last_login_date,last_activity_date,is_admin,melli_code,reshte,ozviat_type from users ORDER by last_login_date DESC")
            for row in curs:
                MN = ""
                if(row[4] != None and str.isnumeric(row[4])):
                    tt = time.gmtime(int(row[4]))
                    MN = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-','/') + " " + str(tt.tm_hour + 3+ ((tt.tm_min+30)//60)) + ":" + str((tt.tm_min + 30)%60))
                if (row[4] == "0"):
                    MN = "--"
                MN2 = ""
                if (row[5] != None and str.isnumeric(row[5])):
                    tt = time.gmtime(int(row[5]))
                    MN2 = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-','/') + " " + str(tt.tm_hour + 3 + ((tt.tm_min+30)//60)) + ":" + str((tt.tm_min + 30)%60))
                if (row[5] == "0"):
                    MN2 = "--"
                rows.append([row[0],row[1],row[2],row[3],MN,MN2,row[6],row[7],row[8],row[9]])

            Excel_Handler.writeTable(["کد عضویت" , "نام و نام خانوادگی","آیدی_عددی_تلگرام" , "شماره تماس" , "زمان آخرین ورود" ,"زمان آخرین فعالیت", "ادمین" , "کدملی" , "رشته" , "سمت"],["A1","B1","C1","D1","E1","F1","G1","H1","I1" ,"J1"] , rows , "exported.xlsx")
            tt = time.gmtime(time.time())
            bot.sendDocument(chat_id,open("exported.xlsx","rb"),caption="`Bot@"+user_data['id']+":~#` "+str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-','/')+ " " + str(tt.tm_hour + 3 + ((tt.tm_min+30)//60)) + ":" + str((tt.tm_min + 30)%60) , parse_mode="markdown")
            return
        if (msg['text'] == "1️⃣فردی1️⃣"):
            set_state(chat_id, "search_via_code")
            bot.sendMessage(chat_id, "❇️لطفا کد عضویت کاربر مورد نظر را وارد نمایید.",reply_to_message_id=msg['message_id'], reply_markup=states[1])
            return
    if(state == "search_via_code"):
        if (content_type != "text"):
            bot.sendMessage(chat_id, "💢لطفا از دکمه ها استفاده نمایید.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "k_mode_sta")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[6])
            return
        user = get_user_by_id(msg['text'])
        if(user==False):
            bot.sendMessage(chat_id,"⛔️کاربر مورد نظر یافت نشد." , reply_to_message_id=msg['message_id'])
            return
        else:
            matn = "`Bot@"+str(user_data['id'])+":~#UserData`\n"
            matn+= "🔻" + "کد عضویت : `" + str(user['id'])+"`\n"
            matn+="🔻" + 'نام و نام خانوادگی : `' + str(user['name'])+"`\n"
            matn += "🔻" + 'کد ملی : `' + str(user['melli_code']) + "`\n"
            matn += "🔻" + 'رشته : `' + str(user['reshte']) + "`\n"
            matn += "🔻" + 'سمت : `' + str(user['ozviat_type']) + "`\n"
            matn+="🔻" + "کد تلگرامی : `" + str(user['tcode'])+"`\n"
            matn+= "🔻" +"شماره تماس : `" + str(user['phno'])+"`\n"
            if(user['last_login_date']!='0'):
                matn+="🔻" + "تاریخ آخرین ورود : `" + get_time_str(user['last_login_date']) + "`\n"
            if(user['last_activity_date']!='0'):
                matn +="🔻" + "تاریخ آخرین فعالیت : `" + get_time_str(user['last_activity_date']) + "`\n\n"
            rrr = get_activitys(user['tcode'])
            if(rrr!=""):
                matn +="🔻" + "**" + "لیست رویداد های شرکت کرده : " + "**\n"
                matn+=rrr
            else:
                matn+="این کاربر در هیچ رویدادی ثبت نام نکرده.‼️"
            bot.sendMessage(chat_id,matn ,parse_mode="markdown", reply_to_message_id= msg['message_id'])
            if(user['photo_id']!=None and user['photo_id']!=""):
                bot.forwardMessage(chat_id , profile_pics_id , user['photo_id'])
            return
    if(state == "get_melli"):
        if(content_type!='text'):
            notfound(chat_id)
            return
        if(is_melli_valid(msg['text'])):
            set_column("users" , "melli_code" , chat_id , msg['text'])
            set_state(chat_id,"main")
            bot.sendMessage(chat_id,"✅کد ملی شما ثبت شد.")
            show_main_keyboard(user_data , msg)
        else:
            bot.sendMessage(chat_id,"❌کد ملی وارد شده معتبر نمیباشد." ,reply_to_message_id=msg['message_id'])
            return
        return
    if (state == "get_phone"):
        if (content_type != 'text'):
            notfound(chat_id)
            return
        if (is_phone_valid(msg['text'])):
            set_column("users", "phno", chat_id, msg['text'])
            set_state(chat_id, "main")
            user_data['phno'] = msg['text']
            bot.sendMessage(chat_id,"✅شماره تماس شما ثبت شد.")
            show_main_keyboard(user_data, msg)
        else:
            bot.sendMessage(chat_id, "❌شماره تماس وارد شده معتبر نمیباشد.", reply_to_message_id=msg['message_id'])
            return
        return

    if(state == 'sta_select'):
        if(content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if(msg['text'] == '🔙برگشت🔙'):
            set_state(chat_id,"main")
            show_main_keyboard(user_data , msg)
        elif (msg['text'] == "➰کاربران➰"):
            set_state(chat_id,"k_mode_sta")
            bot.sendMessage(chat_id,"لطفا حالت مورد نظر را انتخاب نمایید." , reply_to_message_id = msg['message_id'] , reply_markup = states[6])
            return
        elif(msg['text'] == '🎈رویداد ها🎈'):
            if (content_type != "text"):
                bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
                return
            if (Excel_Handler.save_events("events_export.xlsx") == "done"):
                bot.sendDocument(chat_id, open("events_export.xlsx", "rb"), reply_to_message_id=msg['message_id'])
            else:
                bot.sendMessage(chat_id, "⛔️خطایی پیش آمده.")
            return
        elif(msg['text'] == "👨🏻‍💻ادمین ها👨🏻‍💻"):
            if (content_type != "text"):
                bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
                return
            #Send Admins report to bott
            txxxt = get_admins()
            bot.sendMessage(chat_id, txxxt, reply_to_message_id=msg['message_id'],parse_mode="markdown")
            return
        else:
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
        return
    if(state == "sending_msgall"):
        if(content_type == "text"):
            if(msg['text'] == "🔙برگشت🔙"):
                set_state(chat_id,"main")
                show_main_keyboard(user_data,msg)
                return
        set_state(chat_id, "msgall_yon")
        save_data(chat_id, "msg_allid" , msg['message_id'])
        bot.sendMessage(chat_id , "آیا از ارسال پیام بالا اطمینان دارید ؟" , reply_markup= states[4])
        return
    if(state == "msgall_yon"):
        if(content_type!="text"):
            notfound(chat_id)
            return
        if(msg['text'] == "✅بله✅"):
            msg_idd = load_data(chat_id,"msg_allid")
            if(msg_idd != ""):
                send_to_all_2(bot,chat_id,msg_idd)
                save_data(chat_id, "msg_allid" , "")
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
            return
        elif(msg['text'] == "❌خیر❌"):
            set_state(chat_id, "main")
            save_data(chat_id, "msg_allid", "")
            show_main_keyboard(user_data,msg)
            return
        return
    if(state == "ask_exit"):
        if(content_type != "text"):
            notfound(chat_id)
        if(msg['text']=='✅بله✅'):
            set_state(chat_id, "login")
            set_column("users", 'tcode', chat_id, "")
            bot.sendMessage(chat_id, "❎از حساب خود خارج شدید. لطفا گزینه خود را انتخاب کنید.", reply_markup=states[0])
        elif(msg['text'] == '❌خیر❌'):
            set_state(chat_id,"main")
            show_main_keyboard(user_data,msg)
            return
    if(state == 'main'):
        if (get_melli_code_by_id(user_data['id']) in ['-', '', None]):
            set_state(chat_id, "get_melli")
            bot.sendMessage(chat_id, "🔻لطفا کد ملی خود را وارد کنید.", reply_to_message_id=msg['message_id'],reply_markup=ReplyKeyboardRemove())
            return
        if (user_data['phno'] in ['', None]):
            set_state(chat_id, "get_phone")
            bot.sendMessage(chat_id, "🔻لطفا شماره تماس خود را وارد کنید.", reply_to_message_id=msg['message_id'],reply_markup=ReplyKeyboardRemove())
            return
        if(content_type == 'text'):
            if(msg['text'].startswith("/start rem_")):
                if(user_data['is_admin'] == 0):
                    tmp = chat_id
                    chat_id = get_user_data(chat_id)['id']
                    event_id = msg['text'][11:]
                    conn = sqlite3.connect(db_name)
                    query = "update events set sign_ups = ? where id="+str(event_id)
                    sign_ups = get_sign_ups(event_id)
                    if(not str(chat_id) in sign_ups):
                        bot.sendMessage(chat_id,"شما در رویداد مورد نظر شرکت نکرده اید , برای ترک یک رویداد باید ابتدا در آن ثبت نام کنید")
                        return
                    new_sign_ups = ""
                    for i in range(1,len(sign_ups.split(','))):
                        if(sign_ups.split(',')[i] != str(chat_id)):
                            new_sign_ups+=sign_ups.split(',')[i]+","
                    conn.execute(query,[new_sign_ups])
                    conn.commit()
                    chat_id = tmp
                    bot.sendMessage(chat_id, "❎شما رویداد مورد نظر را ترک کردید." , reply_markup=states[2])
                    return
                if(user_data['is_admin'] == 1):
                    event_id = msg['text'][11:]
                    print(event_id)
                    conn = sqlite3.connect(db_name)
                    query = "delete from events where id=" + str(event_id)
                    try:
                        bot.deleteMessage((msgs_id, get_event(event_id)['event_msg_id']))
                    except:
                        pass
                    conn.execute(query)
                    conn.commit()
                    bot.sendMessage(chat_id,"❎رویداد مورد نظر حذف شد")
                    show_main_keyboard(user_data,msg)

            if (msg['text'].startswith("/start show_")):
                try:
                    event_msg_id = msg['text'][12:]
                    bot.forwardMessage(chat_id, msgs_id, event_msg_id)
                    show_main_keyboard(user_data,msg)
                except:
                    bot.sendMessage(chat_id,"یافت نشد")
            if(msg['text'] == '♦️خروج♦️'):
                set_state(chat_id , "ask_exit")
                bot.sendMessage(chat_id, "آیا قصد خروج از حساب خود را دارید ؟" , reply_to_message_id=msg['message_id'] , reply_markup=states[4])
                return
            if(msg['text'] == 'ℹ️مشخصاتℹ️'):
                bot.sendMessage(chat_id,get_info(chat_id , user_data),parse_mode="markdown",reply_to_message_id=msg['message_id'])
                return
            if(msg['text'] == '📭پشتیبانی📭'):
                set_state(chat_id,"talking")
                txxt = """شما در ارتباط با پشتیبانی هستید , لطفا پیام خود را ارسال نمایید , پشتیبانی در اسرع وقت به آن پاسخ خواهد داد.
نکته مهم : بستن قسمت پشتیبانی , مانع رسیدن پیام ادمین ها به شما میشود"""
                bot.sendMessage(chat_id,txxt , reply_markup=states[1])
                return
            if(msg['text'] == "🖊عضویت در رویداد🖊"):
                conn = sqlite3.connect(db_name)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                query = "select event_name,id,sign_ups from events"
                curs = conn.execute(query)
                tmp = chat_id
                chat_id = get_user_data(chat_id)['id']
                for row in curs:
                    if(not str(chat_id) in row[2]):
                        keyboard.inline_keyboard.append([InlineKeyboardButton(text = row[0] , callback_data="event_"+str(row[1]))])
                chat_id = tmp
                if(len(keyboard.inline_keyboard)!=0):
                    bot.sendMessage(chat_id, "لطفا رویداد مورد نظر خود را از لیست پایین انتخاب نمایید",
                                    reply_markup=states[1])
                    bot.sendMessage(chat_id,"🎈رویداد ها🎈" , reply_markup=keyboard)
                    set_state(chat_id,"choosing_event")
                else:
                    bot.sendMessage(chat_id,"❌رویدادی یافت نشد")
            if(msg['text'] == '🗂رویداد های عضو شده🗂') :
                conn = sqlite3.connect(db_name)
                query = "select event_name,id,event_msg_id from events where sign_ups like '%"+str(get_user_data(chat_id)['id'])+"%' limit 70"
                curs = conn.execute(query)
                matn = "رویداد های ثبت نام شده :"+"\n"
                for row in curs:
                    matn += row[0] + " : " + "[" + " حذف رویداد" + "](https://telegram.me/BengC_bot?start=rem_" + str(row[1]) + ") | [" + "مشاهده" + "](https://telegram.me/BengC_bot?start=show_" + str(row[2]) + ")\n"
                if(matn == "رویداد های ثبت نام شده :"+"\n"):
                    bot.sendMessage(chat_id,"شما در رویدادی ثبت نام نکرده اید")
                    return
                else:
                    bot.sendMessage(chat_id, matn , parse_mode="markdown")
                    return
            if(msg['text'] == "➕ثبت رویداد➕" and user_data['is_admin'] == 1):
                bot.sendMessage(chat_id , "لطفا برای رویداد مورد نظر یک نام انتخاب کنید" , reply_to_message_id=msg['message_id'],reply_markup=states[1])
                set_state(chat_id,"enter_event_name")
            if (msg['text'] == "📌پیام همگانی📌" and user_data['is_admin'] == 1):
                set_state(chat_id,"sending_msgall")
                bot.sendMessage(chat_id , "لطفا پیام خود را ارسال کنید" , reply_markup=states[1])
                return
            if(msg['text'] == '🗃پشتیبان🗃' and user_data['is_admin'] == 1):
                bot.sendDocument(chat_id, open("usersdb.db", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Excel_Handler.py", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Userhandle.py", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Bot.py", 'rb'), reply_to_message_id=msg['message_id'])
                return
            if(msg['text'] == '📑مدیریت رویدادها📑' and user_data['is_admin'] == 1):
                text = ""
                conn = sqlite3.connect(db_name)
                query = "select event_name,id,event_msg_id from events"
                curs = conn.execute(query)
                matn = "لیست رویداد ها : " + "\n"
                for row in curs:
                    event = get_event(row[1])
                    matn += row[0]+" ("+str(len([k for k in event['sign_ups'].split(',') if str.isnumeric(k)])) + ") : " + "[" + " حذف رویداد" + "](https://telegram.me/BengC_bot?start=rem_" + str(row[1]) + ") | ["+"مشاهده"+"](https://telegram.me/BengC_bot?start=show_"+str(row[2])+")\n"
                if (matn == "لیست رویداد ها : " + "\n"):
                    bot.sendMessage(chat_id, "رویدادی وجود ندارد")
                    return
                else:
                    bot.sendMessage(chat_id, matn, parse_mode="markdown")
                    return
            if(msg['text'] == '📊گزارش گیری📊' and user_data['is_admin'] == 1):
                set_state(chat_id,"sta_select")
                bot.sendMessage(chat_id,"❗️لطفا بخش مورد نظر خود را انتخاب نمایید" , reply_to_message_id = msg['message_id'] , reply_markup=states[5])

def on_callback_query(msg):
    query_id, from_id, query_data = telepothelli.glance(msg, flavor='callback_query')
    print(msg)
    #print(query_data)
    if (query_data.startswith("1reshte_") and get_user_state(from_id) == "ask_reshte"):
        num = query_data.replace("1reshte_", "")
        kk = ["معماری", "برق", "مکانیک", "نقشه برداری", "ترافیک", "عمران", "سایر"]
        reshte = kk[int(num) - 1]
        chat_id = from_id
        set_column('users', 'reshte', from_id, reshte)
        if (reshte == "سایر"):
            set_state(chat_id, "main")
            user_data = get_user_data(chat_id)
            show_main_keyboard(user_data, msg)
        else:
            set_state(chat_id, "1Dask")
            keyboard = keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='✅بله✅', callback_data="1yep"),
                 InlineKeyboardButton(text='❌خیر❌', callback_data="1Nop")]])
            bot.sendMessage(chat_id, "آیا دانشجویی مقطع کارشناسی هستید ؟", reply_markup=keyboard)
        return
    if (query_data == "1yep" and get_user_state(from_id)=="1Dask"):
        chat_id = from_id
        set_column('users', 'ozviat_type' , chat_id , "دانشجویی")
        set_state(chat_id, "main")
        user_data = get_user_data(chat_id)
        show_main_keyboard(user_data, msg)
        return
    if (query_data == "1Nop" and get_user_state(from_id)=="1Dask"):
        chat_id = from_id
        set_column('users', 'ozviat_type', chat_id, "پیوسته")
        set_state(chat_id, "main")
        user_data = get_user_data(chat_id)
        show_main_keyboard(user_data, msg)
        return
    if(query_data.startswith("reshte_") and get_user_state(from_id)=="reshte_choosing"):
        num = query_data.replace("reshte_" , "")
        kk = ["معماری" , "برق" , "مکانیک" , "نقشه برداری" , "ترافیک" , "عمران" , "سایر"]
        reshte = kk[int(num)-1]
        chat_id = from_id
        save_data(chat_id , "reshte" , reshte)
        if(reshte == "سایر"):
            save_data(chat_id, "ozviat_type", "مهمان")
            set_state(chat_id, 'sending_profile_pic')
            bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        else:
            set_state(chat_id , "Dask")
            keyboard = keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅بله✅' , callback_data = "yep") , InlineKeyboardButton(text='❌خیر❌' , callback_data = "Nop")]])
            bot.sendMessage(chat_id , "آیا دانشجویی مقطع کارشناسی هستید ؟" , reply_markup = keyboard)
        return

    if(query_data == "yep" and get_user_state(from_id)=="Dask"):
        chat_id = from_id
        save_data(from_id , "ozviat_type" , "دانشجویی")
        set_state(chat_id, 'sending_profile_pic')
        bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        return
    if(query_data == "Nop" and get_user_state(from_id)=="Dask"):
        chat_id = from_id
        save_data(from_id , "ozviat_type" , "پیوسته")
        set_state(chat_id, 'sending_profile_pic')
        bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        return
    if(query_data.startswith("yes_")):
        chat_id = query_data.split('_')[1]
        #do some shit here
        bot.sendMessage(chat_id,"فیش شما پذیرفته شد.")
        set_state(chat_id , "entering_name2")
        bot.sendMessage(chat_id,"لطفا نام کامل خود را وارد نمایید (نام و نام خانوادگی)" , reply_markup=ReplyKeyboardRemove())
        bot.sendPhoto(pics_backup , msg['message']['photo'][-1]['file_id'],caption=chat_id)
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    elif(query_data.startswith("no_")):
        chat_id = query_data.split("_")[1]
        bot.sendMessage(chat_id , "فیش شما مورد پذیرش قرار نگرفت , لطفا در صورت اطمینان با پشتیبانی یا ادمین تماس حاصل فرمایید")
        set_state(chat_id,"login")
        bot.sendMessage(chat_id,"لطفا گزینه خود را انتخاب کنید" , reply_markup=states[0])
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    if(query_data.startswith("event_")):
        #dar asl baya in bashe ke aval bebinan rooydad haro bad azashoon beporse ke aya mikhayd ozv beshid ya na vali in movaghatie
        event_id = query_data.split('_')[1]
        event = get_event(event_id)
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        set_state(from_id , "event_yon")
        save_data(from_id , "event_id",event_id)
        bot.forwardMessage(from_id , msgs_id,event['event_msg_id'])
        bot.sendMessage(from_id , "آیا مایلید در رویداد بالا ثبت نام کنید ؟" , reply_markup=states[4])

def register_event(event_id , from_id):
    sign_ups = get_sign_ups(event_id)
    if (sign_ups == "" or sign_ups == None):
        sign_ups += str(get_user_data(from_id)['id'])
    else:
        sign_ups += "," + str(get_user_data(from_id)['id'])
    conn = sqlite3.connect(db_name)
    query = "update events set sign_ups = ? where id = ?"
    conn.execute(query, [sign_ups, int(event_id)])
    conn.commit()


token = "5002577713:AAFvpvix2qiICv1C7MVmxp0JrkjufiIqJlk"

bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)

