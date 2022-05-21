import telepothelli
import telepothelli as telepot
from telepothelli.loop import MessageLoop
from telepothelli.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepothelli.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
import time

import Cart_Handler
import Excel_Handler
import sqlite3

import Userhandle
from Userhandle import *
from persiantools.jdatetime import JalaliDate
import PIL


def get_time_str(t):
    tt = time.gmtime(int(t))
    MN = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-', '/') + " " + str(
        tt.tm_hour + 3 + ((tt.tm_min + 30) // 60)) + ":" + str((tt.tm_min + 30) % 60))
    return MN


db_name = 'usersdb.db'
profile_pics_id = "-"
admins_id = "-"
logging_id = "-"
cart_gp_id = "-"
event_register_id = "-"
moshavere_ids = dict()
moshavere_ids['فنی'] = "-"
moshavere_ids['مالی'] = "-"
moshavere_ids['حقوقی'] = "-"


def is_none_or_empty(st):
    return st == None or st == "" or st == "-"


def Register_Cart(name, ozviat_type, reshte, code, chat_id):
    if (reshte == "عمران"):
        Cart_Handler.Omran_CartCreate(name, ozviat_type, reshte, code, chat_id, "cart1_"+str(chat_id)+".png")
        Cart_Handler.Sakhteman_CartCreate(name, ozviat_type, reshte, code, chat_id, "cart2_"+str(chat_id)+".png")
        caption1 = "#عمران" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('cart1_'+str(chat_id)+'.png', 'rb'), caption1)
        #bot.sendDocument(chat_id, open('cart1.png', 'rb'), caption1)

        caption2 = "#ساختمان" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('cart2_'+str(chat_id)+'.png', 'rb'), caption2)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard.inline_keyboard.append([InlineKeyboardButton(
            text="عمران",
            callback_data="OMRAN_" + str(chat_id))])
        keyboard.inline_keyboard.append([InlineKeyboardButton(
            text="ساختمان",
            callback_data="SAKHTEMAN_" + str(chat_id))])
        bot.sendMessage(cart_gp_id , "کدامیک از کارت های بالا برای کاربر ارسال گردد ؟ " , reply_markup=keyboard)


    else:
        Cart_Handler.Sakhteman_CartCreate(name, ozviat_type, reshte, code, chat_id, "new_cart.png")
        caption2 = "#ساختمان" + "\n" + "نام کامل : " + name + "\nنوع عضویت , سمت : " + ozviat_type + "\nرشته : " + reshte + "\nکد عضویت : " + code
        bot.sendDocument(cart_gp_id, open('new_cart.png', 'rb'), caption2)
        bot.sendDocument(chat_id, open('new_cart.png', 'rb'), caption2)

    return


states = [
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📁میخواهم عضو انجمن شوم📁')], [KeyboardButton(text='✅عضو انجمن های مهندسی هستم✅')],
                                  [KeyboardButton(text='ℹراهنمای رباتℹ'), KeyboardButton(text='ثبت نام رویداد عمومی')]],
                        resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🔙برگشت🔙')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="مشاوره"), KeyboardButton(text='🗂رویداد های عضو شده🗂'),
                                   KeyboardButton(text='🖊عضویت در رویداد🖊')],
                                  [KeyboardButton(text='ویرایش اطلاعات️'), KeyboardButton(text='ℹ️مشخصاتℹ️'),
                                   KeyboardButton(text='📭پشتیبانی📭')],[KeyboardButton(text='♦️خروج♦')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📌پیام همگانی📌'), KeyboardButton(text='📑مدیریت رویدادها📑'),
                                   KeyboardButton(text='➕ثبت رویداد➕')],
                                  [KeyboardButton(text='🗃پشتیبان🗃'), KeyboardButton(text='📊گزارش گیری📊'),
                                   KeyboardButton(text='ℹ️مشخصاتℹ️')],
                                  [KeyboardButton(text='➕ثبت رویداد عمومی➕'), KeyboardButton(text='📌پیام گروهی📌'),
                                   KeyboardButton(text="📄افزودن دستی📄")], [KeyboardButton(text='♦️خروج♦️')]],
                        resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❌خیر❌'), KeyboardButton(text='✅بله✅')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='👨🏻‍💻ادمین ها👨🏻‍💻'), KeyboardButton(text='🎈رویداد ها🎈'),
                                   KeyboardButton(text='🎈رویداد های عمومی🎈'), KeyboardButton(text='➰کاربران➰')],
                                  [KeyboardButton(text='🔙برگشت🔙')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1️⃣فردی1️⃣'), KeyboardButton(text='📂کلی📂')],
                                  [KeyboardButton(text='🔙برگشت🔙')]], resize_keyboard=True),
    ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="آموزشی رایگان"),KeyboardButton(text='📖آموزشی📖'), KeyboardButton(text='🟢رفاهی🟢')],
                                  [KeyboardButton(text='سایر'),KeyboardButton(text= '👟ورزشی👟'), KeyboardButton(text='🔙برگشت🔙')]],
                        resize_keyboard=True),
    ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="حقوقی"), KeyboardButton(text="فنی"), KeyboardButton(text="مالی")],
                  [KeyboardButton(text="🔙برگشت🔙")]], resize_keyboard=True),
    ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📁ثبت نام دانشجویی📁"), KeyboardButton(text="📁ثبت نام عادی📁")]],
        resize_keyboard=True),
    ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="مشاوره خصوصی"), KeyboardButton(text="مشاوره عمومی")],[KeyboardButton(text='🔙برگشت🔙')]],
        resize_keyboard=True),

]


def show_main_keyboard(user_data, msg):
    chat_id = msg['from']['id']
    if (get_melli_code_by_id(user_data['id']) in ['-', '', None]): #TODO add '0000000000'
        set_state(chat_id, "get_melli")
        bot.sendMessage(chat_id, "🔻لطفا کد ملی خود را وارد کنید", reply_to_message_id=msg['message_id'],
                        reply_markup=ReplyKeyboardRemove())
        return
    if (user_data['phno'] in ['', None, '-']): #TODO add '09000000000'
        set_state(chat_id, "get_phone")
        bot.sendMessage(chat_id, "🔻لطفا شماره تلفن خود را وارد کنید", reply_to_message_id=msg['message_id'],
                        reply_markup=ReplyKeyboardRemove())
        return
    if (user_data['reshte'] in ['', None, '-']):
        set_state(chat_id, "ask_reshte")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="مکانیک", callback_data="1reshte_3"),
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
        callback_data="yes_" + str(msg['from']['id']))])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="❌خیر❌",
        callback_data="no_" + str(msg['from']['id']))])
    bot.sendPhoto(chat_id=taeed_channel, photo=msg['photo'][-1]['file_id'],
                  caption="آیا فیش واریزی مورد تایید میباشد ؟", reply_markup=keyboard)
    # bot.sendMessage(taeed_channel ,)

def send_student_card(chat_id , msg):
    msg_id = msg['message_id']
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="✅بله✅",
        callback_data="yems_" + str(msg['from']['id']))])
    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="❌خیر❌",
        callback_data="nmo_" + str(msg['from']['id']))])
    bot.sendPhoto(chat_id=taeed_channel, photo=msg['photo'][-1]['file_id'],
                  caption="آیا کارت دانشجویی مورد تایید میباشد ؟", reply_markup=keyboard)
def notfound(chat_id):
    bot.sendMessage(chat_id, "🔴دستور مورد نظر یافت نشد")


def sendHelp(chat_id, msg):
    bot.sendDocument(chat_id, open("help.pdf", "rb"), caption="فایل راهنمای استفاده از ربات",
                     reply_to_message_id=msg['message_id'])


def handle(msg):
    global states
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(logging_id, str(msg))
    print(content_type)
    print(msg)
    if(content_type=='text'):
        KKL = list(msg['text'])
        ok = True
        if ('۱' in KKL):
            ok = False
        if ('۲' in KKL):
            ok = False
        if ('۳' in KKL):
            ok = False
        if ('۴' in KKL):
            ok = False
        if ('۵' in KKL):
            ok = False
        if ('۶' in KKL):
            ok = False
        if ('۷' in KKL):
            ok = False
        if ('۸' in KKL):
            ok = False
        if ('۹' in KKL):
            ok = False
        if ('۰' in KKL):
            ok = False
        if(not ok):
            bot.sendMessage(chat_id , "🔴لطفا در پیام خود از اعداد فارسی استفاده نکنید. تنها استفاده از ارقام انگلیسی مجاز است.🔴")
            return

    if (str(msg['chat']['id']) in moshavere_ids.values()):
        if ('reply_to_message' in msg and msg['reply_to_message']['from']['is_bot']):
            data = msg['reply_to_message']['text']
            flag = data.split(":")[0]
            if (flag != "*data"):
                return
            send_id, _id, msgid = (data.split(":")[1]).split('_')
            #if (get_user_state(send_id) not in ['talking', "talking2"]):
            #    bot.sendMessage(admins_id, "❌پیام ارسال نشد , کاربر چت را بست",
            #                    reply_to_message_id=msg['message_id'])
             #   return
            try:
                if (content_type == 'text'):
                    bot.sendMessage(send_id, text="Admin (" + msg['from']['first_name'] + "):\n" + msg['text'],
                                    reply_to_message_id=msgid)
                elif (content_type == 'photo'):
                    bot.sendPhoto(send_id, photo=msg['photo'][-1]['file_id'], reply_to_message_id=msgid)
                elif (content_type == 'voice'):
                    bot.sendVoice(send_id, voice=msg['voice']['file_id'], reply_to_message_id=msgid)
                elif (content_type == 'document'):
                    bot.sendDocument(send_id, document=msg['document']['file_id'], reply_to_message_id=msgid)
            except:
                bot.sendMessage(chat_id , "پیام ارسال نشد. ممکن است کاربر از حساب کاربری خود خارج شده باشد یا ربات را حذف کرده باشد.")
            bot.sendMessage(msg['chat']['id'], "done", reply_to_message_id=msg['message_id'])
            return
    if (str(msg['chat']['id']) == admins_id):
        if ('reply_to_message' in msg and msg['reply_to_message']['from']['is_bot']):
            data = msg['reply_to_message']['text']
            flag = data.split(":")[0]
            if (flag != "*data"):
                return
            send_id, _id, msgid = (data.split(":")[1]).split('_')
            #if (get_user_state(send_id) not in ['talking', "talking2"]):
                #bot.sendMessage(admins_id, "❌پیام ارسال نشد , کاربر چت را بست", reply_to_message_id=msg['message_id'])
                #return
            try:
                if (content_type == 'text'):
                    bot.sendMessage(send_id, text="Admin (" + msg['from']['first_name'] + "):\n" + msg['text'],
                                    reply_to_message_id=msgid)
                elif (content_type == 'photo'):
                    bot.sendPhoto(send_id, photo=msg['photo'][-1]['file_id'], reply_to_message_id=msgid)
                elif (content_type == 'voice'):
                    bot.sendVoice(send_id, voice=msg['voice']['file_id'], reply_to_message_id=msgid)
                elif (content_type == 'document'):
                    bot.sendDocument(send_id, document=msg['document']['file_id'], reply_to_message_id=msgid)
            except:
                bot.sendMessage(chat_id , "پیام ارسال نشد. ممکن است کاربر از حساب خود خارج شده یا ربات را حذف کرده باشد")
            bot.sendMessage(admins_id, "done", reply_to_message_id=msg['message_id'])
            return
        if (content_type == "text"):
            if (msg['text'].startswith('.')):
                CMDS = msg['text'].split(' ')
                cmd = CMDS[0]
                if (cmd == ".pic"):
                    # TODO : check user existanse
                    user = get_user_by_id(CMDS[1].replace('\n', ''))
                    if (user == False):
                        bot.sendMessage(admins_id, "❌یافت نشد")
                        return
                    user_chat_id = user['tcode']
                    try:
                        bot.forwardMessage(admins_id, profile_pics_id, message_id=user['photo_id'])
                    except:
                        bot.sendMessage(admins_id, "❌این کاربر عکس پرسنلی ندارد", reply_to_message_id=msg['message_id'])
                if (cmd == ".info"):
                    # TODO : check user exist
                    user = get_user_by_id(CMDS[1].replace('\n', ''))
                    if (user == False):
                        bot.sendMessage(admins_id, "❌یافت نشد")
                        return
                    user_chat_id = user['tcode']

                    bot.sendMessage(admins_id, str(user), reply_to_message_id=msg['message_id'])
                    try:
                        bot.forwardMessage(admins_id, profile_pics_id, message_id=user['photo_id'])
                    except:
                        bot.sendMessage(admins_id, "❌این کاربر عکس پرسنلی ندارد", reply_to_message_id=msg['message_id'])
                if (cmd == ".send"):
                    print(CMDS[1].replace('\n', ''))
                    user = get_user_by_id(CMDS[1].replace('\n', ''))
                    id = user['tcode']
                    if (user == False or id == None or id == ""):
                        bot.sendMessage(admins_id, "❌این اکانت وجود ندارد یا کسی به آن وارد نشده",
                                        reply_to_message_id=msg['message_id'])
                        return
                    txt = " ".join(CMDS[2:])
                    bot.sendMessage(id, text=("Admin (" + msg['from']['first_name'] + ") : \n" + txt))
                    bot.sendMessage(admins_id, 'done✅', reply_to_message_id=msg['message_id'])

                if (cmd == '.sendall'):
                    txt = " ".join(CMDS[1:])
                    send_to_all(bot, "ℹ️Admin (" + msg['from']['first_name'] + ") : \n" + txt)
                    bot.sendMessage(admins_id, 'done', reply_to_message_id=msg['message_id'])
                if (cmd == '.admin'):
                    user = get_user_by_id(CMDS[1].replace('\n', ''))
                    set_column('users', 'is_admin', user['tcode'], 1)
                    bot.sendMessage(admins_id, 'done', reply_to_message_id=msg['message_id'])
                    if (user['tcode'] not in ["", None]):
                        set_state(user['tcode'], "main")
                        bot.sendMessage(user['tcode'], "نوع کاربری شما به ادمین تغییر یافت", reply_markup=states[3])
                    return
                if (cmd == '.unadmin'):
                    user = get_user_by_id(CMDS[1].replace('\n', ''))
                    set_column('users', 'is_admin', user['tcode'], 0)
                    bot.sendMessage(admins_id, 'done', reply_to_message_id=msg['message_id'])
                    if (user['tcode'] not in ["", None]):
                        set_state(user['tcode'], "main")
                        bot.sendMessage(user['tcode'], "نوع کاربری شما به کاربر تغییر یافت", reply_markup=states[2])
                if (cmd == '.help'):
                    bot.sendMessage(admins_id, text=open('help.txt', 'r').read())
                if (cmd == '.remove'):
                    user_id = CMDS[1]
                    Userhandle.removeSTD(user_id)
                    bot.sendMessage(chat_id , "کاربر مورد نظر حذف شد")
                if (cmd == ".exec"):
                    conn = sqlite3.connect(db_name)
                    query = msg['text'][5:]
                    conn.execute(query)
                    conn.commit()
                    bot.sendMessage(chat_id, "done")
                if (cmd == ".show"):
                    stt = ""
                    conn = sqlite3.connect(db_name)
                    query = msg['text'][5:]
                    curs = conn.execute(query)
                    for row in curs:
                        stt += str(row) + "\n"
                    bot.sendMessage(chat_id, stt)

        pass
    if (chat_type != 'private'):  # we don't wanna use bot in a channel
        return
    state = get_user_state(chat_id)
    if (content_type == "text"):
        if (msg['text'] == "/help" or msg['text'] == "ℹراهنمای رباتℹ"):
            sendHelp(chat_id, msg)
            return

    if (state == False or (content_type == 'text' and msg['text'] == "/start")):
        bot.sendMessage(chat_id, "❇️به ربات خوش آمدید", reply_markup=states[0])
        insert_user(chat_id)
        set_state(chat_id, "login")
        sendHelp(chat_id, msg)
        return
        # set_state(chat_id,"entering_code")

    user_data = get_user_data(chat_id)
    print(user_data)
    completed = True
    if (user_data != False):
        if (is_none_or_empty(user_data['photo_id']) or is_none_or_empty(user_data['melli_code']) or is_none_or_empty(
                user_data['reshte'])):
            completed = False
            pass
    set_column("users", "last_activity_date", chat_id, str(int(time.time())))

    if (state == 'waiting'):
        bot.sendMessage(chat_id,
                        "‼رسید شما در حال برسی است. لطفا صبور باشید , به محض تایید شدن , توسط بات به شما پیام داده خواهد شد.")
        return
    if(state == "MOSHAVERETYPE"):
        if(content_type == "text"):
            if(msg['text']=='🔙برگشت🔙'):
                set_state(chat_id , "main")
                show_main_keyboard(user_data , msg)
                return
            if(msg['text'] == "مشاوره خصوصی"):
                set_state(chat_id, "choosing_moshavereT")
            else:
                set_state(chat_id , "gambaloo")
            bot.sendMessage(chat_id, "لطفا از بین لیست زیر قسمت مورد نظر خود را مشخص کنید.", reply_markup=states[8])

        else:
            bot.sendMessage(chat_id , "لطفا از بین گزینه های کیبورد انتخاب کنید.")
        return
    if(state == "entering_student_cart"):
        if (content_type == 'text' and msg['text'] == '🔙برگشت🔙'):
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
            return
        if (content_type == 'photo'):
            send_student_card(chat_id, msg)
            set_state(chat_id, "waiting")
            bot.sendMessage(chat_id, "📌عکس کارت دانشجویی شما به ادمین فرستاده شد. درخواست شما ظرف ۲۴ ساعت اداری بررسی و اقدام میگردد.",reply_markup=ReplyKeyboardRemove())
            return
        else:
            bot.sendMessage(chat_id, "❌لطفا کارت دانشجویی را به صورت عکس ارسال نمایید.")
            return
        return
    if (state == 'login'):
        if (content_type == 'text'):
            if (msg['text'] == '✅عضو انجمن های مهندسی هستم✅'):
                bot.sendMessage(chat_id, "🔻لطفا کد عضویت خود را وارد کنید", reply_markup=states[1])
                set_state(chat_id, "entering_code")
                return
            elif (msg['text'] == '📁میخواهم عضو انجمن شوم📁'):
                set_state(chat_id, "chooseRegisterType")
                bot.sendMessage(chat_id , "لطفا نوع ثبت نام خود را مشخص کنید." , reply_markup=states[9])
                return

            elif (msg['text'] == 'ثبت نام رویداد عمومی'):
                # todo:get list of events wich has not this persons chat_id in them and show them to him
                conn = sqlite3.connect(db_name)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                query = "select id,name,msgid,signedtcodes from events2"
                curs = conn.execute(query)
                for row in curs:
                    if (row[3] == None or (not str(chat_id) in row[3])):
                        keyboard.inline_keyboard.append(
                            [InlineKeyboardButton(text=row[1], callback_data="event2_" + str(row[0]))])
                if (len(keyboard.inline_keyboard) != 0):
                    bot.sendMessage(chat_id, "لطفا رویداد مورد نظر خود را از لیست پایین انتخاب نمایید",
                                    reply_markup=states[1])
                    bot.sendMessage(chat_id, "🎈رویداد های عمومی🎈", reply_markup=keyboard)
                    set_state(chat_id, "choosing_event2")
                else:
                    bot.sendMessage(chat_id, "❌رویدادی یافت نشد")
                pass
            else:
                notfound(chat_id)
                return
        else:
            notfound()
            return
    if (state == "choosing_event2" and content_type == 'text' and msg['text'] == '🔙برگشت🔙'):
        set_state(chat_id, "login")
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
        return
    if (state == 'sending_fish'):
        if (content_type == 'text' and msg['text'] == '🔙برگشت🔙'):
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
            return
        if (content_type == 'photo'):
            # must do some shit here
            send_fish(chat_id, msg)
            set_state(chat_id, "waiting")
            bot.sendMessage(chat_id, "📌درخواست شما ظرف ۲۴ ساعت اداری بررسی و اقدام میگردد.",
                            reply_markup=ReplyKeyboardRemove())
            return
        else:
            bot.sendMessage(chat_id, "❌لطفا فیش واریزی را به صورت عکس ارسال نمایید.")
            return
    if (state == 'entering_code'):
        if (content_type == 'text'):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "login")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
                return
            print(get_user_by_column('id', msg['text']))
            if (len(get_user_by_column("id", msg['text'])) == 0):
                bot.sendMessage(chat_id, "❌کد عضویت مورد نظر وجود ندارد.")
                return
            else:
                bot.sendMessage(chat_id, "❇️لطفا نام کامل خود را وارد کنید.")
                set_state(chat_id, "entering_name")
                set_column('users2', 'id', chat_id, msg['text'])
                return
        else:
            bot.sendMessage(chat_id, "❗️لطفا کد عضویت خود را به صورت متن وارد نمایید.")
    if(state == "chooseRegisterType"):
        if(content_type == 'text'):
            if(msg['text']=="📁ثبت نام دانشجویی📁"):
                set_column('users', 'ozviat_type', chat_id, "دانشجویی")
                save_data(chat_id, "ozviat_type", "دانشجویی")
                bot.sendMessage(chat_id , "لطفا عکس کارت دانشجویی خود را بارگزاری کنید." , reply_markup=states[1])
                set_state(chat_id , "entering_student_cart")
                return
            elif(msg['text'] == "📁ثبت نام عادی📁"):
                bot.sendMessage(chat_id,
                                "لطفا مبلغ 350,000 تومان را به شماره حساب :\n" + "5022 2913 0240 6226\n" + "به نام محمد شریفی(امور مالی) واریز نموده و تصویر رسید واریزی را ارسال نمایید.",
                                reply_markup=states[1])
                set_column('users', 'ozviat_type', chat_id, "پیوسته")
                set_state(chat_id, "sending_fish")
                save_data(chat_id, "ozviat_type", "پیوسته")
        else:
            bot.sendMessage(chat_id , "لطفا از بین گزینه های موجود انتخاب نمایید")
        return
    if(state =="hamrahYON"):
        if(content_type == 'text'):
            if(msg['text'] == "✅بله✅"):
                bot.sendMessage(chat_id , "لطفا نام کامل همراه خود را وارد نمایید." , reply_markup=states[1])
                set_state(chat_id , "getting_hamrah_name")


            if(msg['text'] == "❌خیر❌"):
                set_state(chat_id, "main")
                ev = Userhandle.get_event(load_data(chat_id, "event_id"))
                if (ev['event_type'] != "آموزشی"):
                    register_event(load_data(chat_id, "event_id"), chat_id)
                    bot.sendMessage(chat_id, "✅در رویداد مورد نظر با موفقیت عضو شدید.",
                                    reply_to_message_id=msg['message_id'])
                    show_main_keyboard(user_data, msg)
                else:
                    set_state(chat_id, "event_fish")
                    bot.sendMessage(chat_id, "لطفا مبلغ دوره را واریز نموده و عکس رسید واریزی را ارسال نمایید",
                                    reply_markup=states[1])
        else:
            bot.sendMessage(chat_id , "لطفا از بین گزینه های منو انتخاب نمایید")
        return
    if(state == "getting_hamrah_name"):
        if(content_type == 'text'):
            hamrah = msg['text']
            save_data(chat_id,"hamrahName" , hamrah)
            bot.sendMessage(chat_id , "لطفا کد ملی همراه خود را وارد نمایید")
            set_state(chat_id , "hamrahMelliCode")
        else:
            print("لطفا نام کامل فرد همراه را وارد کنید.")
        return
    if(state == "hamrahMelliCode"):
        if(content_type == 'text'):
            melli_code = msg['text']
            save_data(chat_id , "hamrahMelliCode" , melli_code)
            set_state(chat_id, "main")
            ev = Userhandle.get_event(load_data(chat_id, "event_id"))
            if (ev['event_type'] != "آموزشی"):
                register_eventS(load_data(chat_id, "event_id"), chat_id , load_data(chat_id , "hamrahName") , load_data(chat_id , "hamrahMelliCode"))

                bot.sendMessage(chat_id, "✅در رویداد مورد نظر با موفقیت عضو شدید.",
                                reply_to_message_id=msg['message_id'])
                show_main_keyboard(user_data, msg)

            else:

                set_state(chat_id, "event_fish")
                bot.sendMessage(chat_id, "لطفا مبلغ دوره را واریز نموده و عکس رسید واریزی را ارسال نمایید",
                                reply_markup=states[1])
        else:
            bot.sendMessage(chat_id , "لطفا متن وارد کنید")
    if (state == "entering_name"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❗️لطفا نام و نام خانوادگی خود را تایپ کنید.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
            return
        if (is_name_valid(chat_id, msg['text'], get_value("users2", chat_id, 'id')) != False):
            # sec bug : any person that logs in with the second account can change the owner ship of it (is it bug or feature ?)
            query = "update users set tcode = ? where id = ?"  # register the row with this person
            conn = sqlite3.connect(db_name)
            conn.execute(query, [str(chat_id), get_value('users2', chat_id, 'id')])
            conn.commit()
            set_state(chat_id, "main")
            set_column("users", "last_login_date", chat_id, str(int(time.time())))
            bot.sendMessage(chat_id, "✅ورود با موفقیت انجام شد.")
            user_data = get_user_data(chat_id)
            show_main_keyboard(user_data, msg)
            # bot.sendMessage(chat_id,"لطفا گزینه مورد نظر را انتخاب کنید" , reply_markup= states[2])
            return
        else:
            bot.sendMessage(chat_id, "❌نام وارد شده با کدعضویت مطابق نیست.")
            return

    if (user_data == False and get_user_state(chat_id) == False):
        bot.sendMessage(chat_id, "❌خطایی پیش آمده.")
        return
    if (state == 'entering_name2'):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "‼️لطفا نام و نام خانوادگی کامل خود را به صورت متن وارد نمایید.")
            return
        else:
            fullname = msg['text'].replace('\n', ' ')  # age name ro to ye khat , family ro to ye khat zad bugy nashe
            if (not check_name(fullname)):
                bot.sendMessage(chat_id, "‼️نام وارد شده معتبر نیست. فقط از حروف فارسی میتوانید استفاده کنید.")
                return

            # save fullname to somewheree
            save_data(chat_id, "name", fullname)
            set_state(chat_id, 'reshte_choosing')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="مکانیک", callback_data="reshte_3"),
                 InlineKeyboardButton(text="برق", callback_data="reshte_2"),
                 InlineKeyboardButton(text="معماری", callback_data="reshte_1")],
                [InlineKeyboardButton(text="عمران", callback_data="reshte_6"),
                 InlineKeyboardButton(text="ترافیک", callback_data="reshte_5"),
                 InlineKeyboardButton(text="نقشه برداری", callback_data="reshte_4")],
                [InlineKeyboardButton(text="سایر", callback_data="reshte_7")]])
            bot.sendMessage(chat_id, "لطفا رشته خود را انتخاب نمایید", reply_markup=keyboard)
        return
        pass
    if (state == 'sending_profile_pic'):
        if (content_type != 'photo'):
            bot.sendMessage(chat_id, "‼️باید عکس ارسال کنید , ارسال فایل یا متن و .. غیرمجاز میباشد.")
            return
        # TODO : check if the pic is valid or not (face recognition)
        bot.download_file(file_id=msg['photo'][-1]['file_id'], dest="prof_pic+" + str(chat_id) + ".jpg")
        image = PIL.Image.open("prof_pic+" + str(chat_id) + ".jpg")
        width, height = image.size
        # if(abs((width/height)-(0.75))>1e-1):
        # bot.sendMessage(chat_id,"ابعاد عکس مورد نظر تایید نشد, لطفا از 3 در 4 بودن عکس اطمینان حاصل فرمایید" + "‼️" , reply_to_message_id = msg['message_id'])
        # return
        new_msg = bot.forwardMessage(profile_pics_id, chat_id, msg['message_id'])
        code = register_code(load_data(chat_id, "reshte"))
        name = load_data(chat_id, "name")
        insert_users(code, name, chat_id, "")
        ozviat_type = load_data(chat_id, "ozviat_type")
        set_column('users', 'ozviat_type', chat_id, ozviat_type)
        reshte = load_data(chat_id, "reshte")
        set_column('users', 'reshte', chat_id, reshte)
        set_column('users', 'photo_id', chat_id, str(new_msg['message_id']))
        set_column('users', 'tcode', chat_id, str(chat_id))
        bot.sendMessage(chat_id, "✅عکس پرسنلی ذخیره شد. کد عضویت شما : " + code)
        bot.sendMessage(chat_id, "درحال تولید و ارسال کارت عضویت برای چاپ...")
        Register_Cart(name, ozviat_type, reshte, code, chat_id)
        set_state(chat_id, "main")
        show_main_keyboard(get_user_data(chat_id) , msg)
        #bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
        pass
    if (content_type == 'text'):
        if (msg['text'] == '/keyboard'):
            set_state(chat_id, 'main')
            show_main_keyboard(user_data, msg)
    if (state == 'talking'):
        if (content_type == 'text'):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
                return
        mm = bot.forwardMessage(admins_id, chat_id, msg['message_id'])
        bot.sendMessage(admins_id, "*data:" + str(chat_id) + "_" + str(user_data['id']) + "_" + str(msg['message_id']),
                        reply_to_message_id=mm['message_id'])
        return
    if (state == 'talking2'):
        if (content_type == 'text'):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
                return
        idd = load_data(chat_id, "moshavere_id")
        mm = bot.forwardMessage(idd, chat_id, msg['message_id'])
        bot.sendMessage(idd, "*data:" + str(chat_id) + "_" + str(user_data['id']) + "_" + str(msg['message_id']),
                        reply_to_message_id=mm['message_id'])
        return
    if (user_data == False and state == 'main'):
        bot.sendMessage(chat_id, "🛑شما از اکانت خود خارج شدید. لطفا برای استفاده از ربات , دوباره وارد شوید.")
        set_state(chat_id, "login")
        bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[0])
        return

    if (state == 'choosing_event'):
        if (content_type == "text"):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
            else:
                bot.sendMessage(chat_id, "🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return
        else:
            bot.sendMessage(chat_id, "🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return

    if (state == "choosing_moshavereT"):
        noe = ""
        if (content_type == "text"):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
            elif msg['text'] in ["فنی", "مالی", "حقوقی"]:  # TODO : update list
                noe = msg['text']
                set_state(chat_id, "talking2")
                save_data(chat_id, "moshavere_id", moshavere_ids[noe])
                txxt = """شما در ارتباط با پشتیبانی هستید , لطفا پیام خود را ارسال نمایید , پشتیبانی در اسرع وقت به آن پاسخ خواهد داد.
                                        """
                bot.sendMessage(chat_id, txxt, reply_markup=states[1])
            return
        else:
            bot.sendMessage(chat_id, "🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return
    if (state == "gambaloo"):
        noe = ""
        if (content_type == "text"):
            if (msg['text'] == '🔙برگشت🔙'):
                set_state(chat_id, "main")
                bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[2])
                return
            elif msg['text'] in ["فنی", "مالی", "حقوقی"]:  # TODO : update list
                noe = msg['text']
                txt = Userhandle.get_link(noe)
                bot.sendMessage(chat_id, "لینک گروه جهت عضویت : " + "\n" + txt)
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
            return
        else:
            bot.sendMessage(chat_id, "🛑گزینه خود را انتخاب کرده یا از بازگشت استفاده نمایید.")
            return
        return
    if (state == "enter_event_name"):
        if (content_type != "text"):
            bot.sendMessage(chat_id, "‼️نام رویداد تنها میتواند به صورت متنی باشد. از ارسال مدیا خودداری فرمایید.",
                            reply_to_message_id=msg['message_id'])
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "main")
            save_data(chat_id, "new_event_type", "")
            show_main_keyboard(user_data, msg)
            return
        else:
            save_data(chat_id, "event_name", msg['text'])
            set_state(chat_id, "event_enter")
            bot.sendMessage(chat_id,
                            "✅نام رویداد انتخاب شد. لطفا یک پیام (میتواند شامل یک عکس با کپشن یا تنها کپشن خالی باشد) برای محتویات رویداد ارسال نمایید. دقت فرمایید که اگر رویداد مورد نظر جزو خدمات آموزشی میباشد تعیین قیمت دوره در متن پیام دوره ذکر شود.",
                            reply_to_message_id=msg['message_id'], reply_markup=states[1])
        return
    if (state == "event2start"):
        if (content_type != "text"):
            bot.sendMessage(chat_id, "‼️نام رویداد تنها میتواند به صورت متنی باشد. از ارسال مدیا خودداری فرمایید.",
                            reply_to_message_id=msg['message_id'])
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "main")
            show_main_keyboard(user_data, msg)
            return
        else:
            save_data(chat_id, "event2_name", msg['text'])
            set_state(chat_id, "event2_enter")
            bot.sendMessage(chat_id,
                            "✅نام رویداد انتخاب شد. لطفا یک پیام (میتواند شامل یک عکس با کپشن یا تنها کپشن خالی باشد) برای محتویات رویداد ارسال نمایید.",
                            reply_to_message_id=msg['message_id'], reply_markup=states[1])
        return
    if (state == "event2_enter"):
        mm = bot.forwardMessage(msgs_id, chat_id, msg['message_id'])
        insert_event2(load_data(chat_id, "event2_name"), mm['message_id'])
        set_state(chat_id, "main")
        bot.sendMessage(chat_id, "✅رویداد مورد نظر با موفقیت ثبت شد.", reply_to_message_id=msg['message_id'])
        show_main_keyboard(user_data, msg)
    if (state == "event_enter"):
        mm = bot.forwardMessage(msgs_id, chat_id, msg['message_id'])
        insert_event(load_data(chat_id, "event_name"), mm['message_id'], load_data(chat_id, "new_event_type"))
        set_state(chat_id, "main")
        bot.sendMessage(chat_id, "✅رویداد مورد نظر با موفقیت ثبت شد.", reply_to_message_id=msg['message_id'])
        show_main_keyboard(user_data, msg)
    if (state == "event_fish"):
        if (content_type == "text"):
            if (msg['text'] == "🔙برگشت🔙"):
                set_state(chat_id, "main")
                save_data(chat_id, "new_event_type", "")
                show_main_keyboard(user_data, msg)
                return
            return
        if (content_type != 'photo'):
            bot.sendMessage(chat_id, "‼️باید عکس ارسال کنید , ارسال فایل یا متن و .. غیرمجاز میباشد.")
            return
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[])
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text="✅بله✅",
                callback_data="ye2s_" + str(get_user_data(chat_id)['id']) + "_" + load_data(chat_id, "event_id"))])
            keyboard.inline_keyboard.append([InlineKeyboardButton(
                text="❌خیر❌",
                callback_data="n2o_" + str(get_user_data(chat_id)['id']) + "_" + load_data(chat_id, "event_id"))])

            bot.sendPhoto(chat_id=event_register_id, photo=msg['photo'][-1]['file_id'],
                          caption="آیا فیش واریزی مورد تایید میباشد ؟", reply_markup=keyboard)
            bot.sendMessage(chat_id,
                            "رسید واریزی شما ارسال شد و پس از تایید خبر عضویت یا عدم عضویت به شما ارسال خواهد شد.")
            set_state(chat_id, "main")
            show_main_keyboard(user_data, msg)
            # TODO:send fish with yes or no button to a channel
            pass

    if (state == "event_yon"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "🛑لطفا از بین گزینه های کیبورد انتخاب نمایید!")
            return
        else:
            if (msg['text'] == '❌خیر❌'):
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
            if (msg['text'] == '✅بله✅'):
                event = Userhandle.get_event(load_data(chat_id , "event_id"))
                if (event["event_type"] == "ورزشی"):
                    set_state(chat_id, "hamrahYON")
                    bot.sendMessage(chat_id, "آیا همراه دارید ؟", reply_markup=states[4])
                    return

                set_state(chat_id, "main")
                ev = Userhandle.get_event(load_data(chat_id, "event_id"))
                if (ev['event_type'] != "آموزشی"):
                    register_event(load_data(chat_id, "event_id"), chat_id)
                    bot.sendMessage(chat_id, "✅در رویداد مورد نظر با موفقیت عضو شدید.",
                                    reply_to_message_id=msg['message_id'])
                    show_main_keyboard(user_data, msg)
                else:
                    set_state(chat_id, "event_fish")
                    bot.sendMessage(chat_id, "لطفا مبلغ دوره را واریز نموده و عکس رسید واریزی را ارسال نمایید",
                                    reply_markup=states[1])
    if (state == "event2_yon"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "🛑لطفا از بین گزینه های کیبورد انتخاب نمایید!")
            return
        else:
            if (msg['text'] == '❌خیر❌'):
                set_state(chat_id, "login")
                bot.sendMessage(chat_id, "لطفا گزینه مورد نظر را انتخاب نمایید", reply_markup=states[0])
                return
            if (msg['text'] == '✅بله✅'):
                set_state(chat_id, "getevname")
                bot.sendMessage(chat_id, "لطفا نام کامل خود را وارد کنید", reply_markup=states[1])
    if (state == "getevname"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "لطفا گزینه مورد نظر را انتخاب نمایید", reply_markup=states[0])
            return
        else:
            save_data(chat_id, "evname", msg['text'])
            set_state(chat_id, "getevphone")
            bot.sendMessage(chat_id, "لطفا شماره تفلن خود را وارد نمایید", reply_markup=states[1])
            return
    if (state == "getevphone"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "لطفا گزینه مورد نظر را انتخاب نمایید", reply_markup=states[0])
            return
        else:
            save_data(chat_id, "phone_number", msg['text'])
            register_event3(chat_id, load_data(chat_id, "event2_id"), load_data(chat_id, "phone_number"),
                            load_data(chat_id, "evname"))
            bot.sendMessage(chat_id, "✅در رویداد مورد نظر با موفقیت عضو شدید.",
                            reply_to_message_id=msg['message_id'])
            set_state(chat_id, "login")
            bot.sendMessage(chat_id, "لطفا گزینه مورد نظر را انتخاب نمایید", reply_markup=states[0])
    if (state == "k_mode_sta"):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "sta_select")
            bot.sendMessage(chat_id, "🌐لطفا بخش مورد نظر خود را انتخاب نمایید.", reply_to_message_id=msg['message_id'],
                            reply_markup=states[5])
            return

        if (msg['text'] == "📂کلی📂"):
            rows = []
            conn = sqlite3.connect(db_name)
            curs = conn.execute(
                "select id,name,tcode,phno,last_login_date,last_activity_date,is_admin,melli_code,reshte,ozviat_type from users ORDER by last_login_date DESC")
            for row in curs:
                MN = ""
                if (row[4] != None and str.isnumeric(row[4])):
                    tt = time.gmtime(int(row[4]))
                    MN = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-',
                                                                                                                 '/') + " " + str(
                        tt.tm_hour + 3 + ((tt.tm_min + 30) // 60)) + ":" + str((tt.tm_min + 30) % 60))
                if (row[4] == "0"):
                    MN = "--"
                MN2 = ""
                if (row[5] != None and str.isnumeric(row[5])):
                    tt = time.gmtime(int(row[5]))
                    MN2 = str(str(JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-',
                                                                                                                  '/') + " " + str(
                        tt.tm_hour + 3 + ((tt.tm_min + 30) // 60)) + ":" + str((tt.tm_min + 30) % 60))
                if (row[5] == "0"):
                    MN2 = "--"
                rows.append([row[0], row[1], row[2], row[3], MN, MN2, row[6], row[7], row[8], row[9]])

            Excel_Handler.writeTable(
                ["کد عضویت", "نام و نام خانوادگی", "آیدی_عددی_تلگرام", "شماره تماس", "زمان آخرین ورود",
                 "زمان آخرین فعالیت", "ادمین", "کدملی", "رشته", "سمت"],
                ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1"], rows, "exported.xlsx")
            tt = time.gmtime(time.time())
            bot.sendDocument(chat_id, open("exported.xlsx", "rb"), caption="`Bot@" + user_data['id'] + ":~#` " + str(
                JalaliDate.to_jalali(year=tt.tm_year, month=tt.tm_mon, day=tt.tm_mday)).replace('-', '/') + " " + str(
                tt.tm_hour + 3 + ((tt.tm_min + 30) // 60)) + ":" + str((tt.tm_min + 30) % 60), parse_mode="markdown")
            return
        if (msg['text'] == "1️⃣فردی1️⃣"):
            set_state(chat_id, "search_via_code")
            bot.sendMessage(chat_id, "❇️لطفا کد عضویت کاربر مورد نظر را وارد نمایید.",
                            reply_to_message_id=msg['message_id'], reply_markup=states[1])
            return
    if (state == "search_via_code"):
        if (content_type != "text"):
            bot.sendMessage(chat_id, "💢لطفا از دکمه ها استفاده نمایید.")
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "k_mode_sta")
            bot.sendMessage(chat_id, "🟢گزینه مورد نظر را انتخاب کنید", reply_markup=states[6])
            return
        user = get_user_by_id(msg['text'])
        if (user == False):
            bot.sendMessage(chat_id, "⛔️کاربر مورد نظر یافت نشد.", reply_to_message_id=msg['message_id'])
            return
        else:
            matn = "`Bot@" + str(user_data['id']) + ":~#UserData`\n"
            matn += "🔻" + "کد عضویت : `" + str(user['id']) + "`\n"
            matn += "🔻" + 'نام و نام خانوادگی : `' + str(user['name']) + "`\n"
            matn += "🔻" + 'کد ملی : `' + str(user['melli_code']) + "`\n"
            matn += "🔻" + 'رشته : `' + str(user['reshte']) + "`\n"
            matn += "🔻" + 'سمت : `' + str(user['ozviat_type']) + "`\n"
            matn += "🔻" + "کد تلگرامی : `" + str(user['tcode']) + "`\n"
            matn += "🔻" + "شماره تماس : `" + str(user['phno']) + "`\n"
            if (user['last_login_date'] != '0'):
                matn += "🔻" + "تاریخ آخرین ورود : `" + get_time_str(user['last_login_date']) + "`\n"
            if (user['last_activity_date'] != '0'):
                matn += "🔻" + "تاریخ آخرین فعالیت : `" + get_time_str(user['last_activity_date']) + "`\n\n"
            rrr = get_activitys(user['tcode'])
            if (rrr != ""):
                matn += "🔻" + "**" + "لیست رویداد های شرکت کرده : " + "**\n"
                matn += rrr
            else:
                matn += "این کاربر در هیچ رویدادی ثبت نام نکرده.‼️"
            bot.sendMessage(chat_id, matn, parse_mode="markdown", reply_to_message_id=msg['message_id'])
            if (user['photo_id'] != None and user['photo_id'] != ""):
                try:
                    bot.forwardMessage(chat_id, profile_pics_id, user['photo_id'])
                except:
                    bot.sendMessage(chat_id, "عکس پرسنلی یافت نشد")
            return
    if (state == "get_melli"):
        if (content_type != 'text'):
            notfound(chat_id)
            return
        if (is_melli_valid(msg['text'])):
            set_column("users", "melli_code", chat_id, msg['text'])
            set_state(chat_id, "main")
            bot.sendMessage(chat_id, "✅کد ملی شما ثبت شد.")
            show_main_keyboard(user_data, msg)
        else:
            bot.sendMessage(chat_id, "❌کد ملی وارد شده معتبر نمیباشد.", reply_to_message_id=msg['message_id'])
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
            bot.sendMessage(chat_id, "✅شماره تماس شما ثبت شد.")
            show_main_keyboard(user_data, msg)
        else:
            bot.sendMessage(chat_id, "❌شماره تماس وارد شده معتبر نمیباشد.", reply_to_message_id=msg['message_id'])
            return
        return

    if (state == 'sta_select'):
        if (content_type != 'text'):
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
            return
        if (msg['text'] == '🔙برگشت🔙'):
            set_state(chat_id, "main")
            show_main_keyboard(user_data, msg)
        elif (msg['text'] == "➰کاربران➰"):
            set_state(chat_id, "k_mode_sta")
            bot.sendMessage(chat_id, "لطفا حالت مورد نظر را انتخاب نمایید.", reply_to_message_id=msg['message_id'],
                            reply_markup=states[6])
            return
        elif (msg['text'] == '🎈رویداد های عمومی🎈'):
            if (content_type != "text"):
                bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
                return
            if (Excel_Handler.save_events2("events_oomoomi_export.xlsx") == "done"):
                bot.sendDocument(chat_id, open("events_oomoomi_export.xlsx", "rb"),
                                 reply_to_message_id=msg['message_id'])
            else:
                bot.sendMessage(chat_id, "⛔️خطایی پیش آمده.")
            return
        elif (msg['text'] == '🎈رویداد ها🎈'):
            if (content_type != "text"):
                bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
                return
            if (Excel_Handler.save_events("events_export.xlsx") == "done"):
                bot.sendDocument(chat_id, open("events_export.xlsx", "rb"), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id , open("usersdb.db" , "rb") , reply_to_message_id=msg['message_id'] , caption = "فایل خروجی برای برنامه DataBase Viewer")

            else:
                bot.sendMessage(chat_id, "⛔️خطایی پیش آمده.")
            return
        elif (msg['text'] == "👨🏻‍💻ادمین ها👨🏻‍💻"):
            if (content_type != "text"):
                bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
                return
            # Send Admins report to bott
            txxxt = get_admins()
            bot.sendMessage(chat_id, txxxt, reply_to_message_id=msg['message_id'], parse_mode="markdown")
            return
        else:
            bot.sendMessage(chat_id, "❌دستور مورد نظر یافت نشد.")
        return
    if (state == "sending_msgall"):
        if (content_type == "text"):
            if (msg['text'] == "🔙برگشت🔙"):
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
        set_state(chat_id, "msgall_yon")
        save_data(chat_id, "msg_allid", msg['message_id'])
        bot.sendMessage(chat_id, "آیا از ارسال پیام بالا اطمینان دارید ؟", reply_markup=states[4])
        return
    if (state == "sending_msgone"):
        if (content_type == "text"):
            if (msg['text'] == "🔙برگشت🔙"):
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
        set_state(chat_id, "msgone_yon")
        save_data(chat_id, "msg_oneid", msg['message_id'])
        bot.sendMessage(chat_id, "آیا از ارسال پیام بالا اطمینان دارید ؟", reply_markup=states[4])
        return
    if (state == "choosing_eventtype"):
        if (content_type != "text"):
            notfound(chat_id)
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "main")
            show_main_keyboard(user_data, msg)
            return
        _type = msg['text']
        if (_type == "📖آموزشی📖"):
            _type = "آموزشی"
        if(_type == "آموزشی رایگان"):
            _type = "آموزشی رایگان"
        if (_type == '🟢رفاهی🟢'):
            _type = "رفاهی"
        if (_type == "سایر"):
            _type = "سایر"
        if(_type == "👟ورزشی👟"):
            _type = "ورزشی"

        save_data(chat_id, "new_event_type", _type)
        set_state(chat_id, "enter_event_name")
        bot.sendMessage(chat_id, "لطفا نام رویداد را انتخاب نمایید.", reply_markup=states[1])

    if (state == "ozviatEnter"):
        if (content_type != "text"):
            notfound(chat_id)
            return
        if (msg['text'] == "🔙برگشت🔙"):
            set_state(chat_id, "main")
            save_data(chat_id, "msg_oneid", "")
            show_main_keyboard(user_data, msg)
            return
        ress = ""
        entered_ids = msg['text'].split('\n')
        for entered_id in entered_ids:
            send_chatid = Userhandle.get_chat_id(entered_id)
            if (not (send_chatid in ['', None, ""])):
                bot.sendMessage(send_chatid, "پیام ارسال شده از طرف ادمین : ")
                bot.forwardMessage(send_chatid, chat_id, load_data(chat_id, "msg_oneid"))
                ress+="کد عضویت : " +str(entered_id)+"\nنام : "+Userhandle.get_user_data_by_id(entered_id)['name']+"\n"+ "پیام مورد نظر ارسال شد."+"\n\n"
                #return
            else:
                ress+= "خطا. از صحت کد عضویت یا اکانت داشتن آن اطمینان حاصل فرمایید!" + "\nکد عضویت : "+str(entered_id)
                #return
        save_data(chat_id, "msg_oneid", "")
        set_state(chat_id, "main")
        bot.sendMessage(chat_id , ress)
        show_main_keyboard(user_data, msg)
        return

    if (state == "msgone_yon"):
        if (content_type != "text"):
            notfound(chat_id)
            return
        if (msg['text'] == "✅بله✅"):
            msg_idd = load_data(chat_id, "msg_oneid")
            if (msg_idd != ""):
                set_state(chat_id, "ozviatEnter")
                bot.sendMessage(chat_id, "لطفا کد عضویت گیرنده های پیام را وارد نمایید(در هر خط یک کد عضویت وارد شده و از وارد کردن چیزی بجز کد عضویت پرهیز شود).",
                                reply_to_message_id=msg['message_id'], reply_markup=states[1])
                return
            return
        elif (msg['text'] == "❌خیر❌"):
            set_state(chat_id, "main")
            save_data(chat_id, "msg_allid", "")
            show_main_keyboard(user_data, msg)
            return
        return

    if (state == "msgall_yon"):
        if (content_type != "text"):
            notfound(chat_id)
            return
        if (msg['text'] == "✅بله✅"):
            msg_idd = load_data(chat_id, "msg_allid")
            if (msg_idd != ""):
                send_to_all_2(bot, chat_id, msg_idd)
                save_data(chat_id, "msg_allid", "")
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
            return
        elif (msg['text'] == "❌خیر❌"):
            set_state(chat_id, "main")
            save_data(chat_id, "msg_allid", "")
            show_main_keyboard(user_data, msg)
            return
        return
    if (state == "ask_exit"):
        if (content_type != "text"):
            notfound(chat_id)
        if (msg['text'] == '✅بله✅'):
            set_state(chat_id, "login")
            set_column("users", 'tcode', chat_id, "")
            bot.sendMessage(chat_id, "❎از حساب خود خارج شدید. لطفا گزینه خود را انتخاب کنید.", reply_markup=states[0])
        elif (msg['text'] == '❌خیر❌'):
            set_state(chat_id, "main")
            show_main_keyboard(user_data, msg)
            return
    if (state == "afzudan"):
        if (content_type == "text"):
            if (msg['text'] == "🔙برگشت🔙"):
                set_state(chat_id, "main")
                show_main_keyboard(user_data, msg)
                return
        if (content_type == "document"):
            if (msg['document']['file_name'][-4:] == "xlsx"):
                bot.download_file(file_id=msg['document']['file_id'], dest="add.xlsx")
                Userhandle.importToDB(bot, chat_id, msg, "add.xlsx")
            else:
                bot.sendMessage(chat_id, "فایل ارسال شده از نوع قالب نیست!")
            return
        else:
            bot.sendMessage(chat_id,
                            "لطفا فایل اکسل قالب را پر کرده و ارسال نمایید. ارسال نوع های دیگه پیام مجاز نیست!")
        return
    if (state == 'main'):
        if (get_melli_code_by_id(user_data['id']) in ['-', '', None]):
            set_state(chat_id, "get_melli")
            bot.sendMessage(chat_id, "🔻لطفا کد ملی خود را وارد کنید.", reply_to_message_id=msg['message_id'],
                            reply_markup=ReplyKeyboardRemove())
            return
        if (user_data['phno'] in ['', None]):
            set_state(chat_id, "get_phone")
            bot.sendMessage(chat_id, "🔻لطفا شماره تماس خود را وارد کنید.", reply_to_message_id=msg['message_id'],
                            reply_markup=ReplyKeyboardRemove())
            return
        if (content_type == 'text'):
            if (msg['text'].startswith("/start rem2_")):
                if (user_data['is_admin'] == 1):
                    event_id = msg['text'][12:]
                    conn = sqlite3.connect(db_name)
                    query = "delete from events2 where id=" + str(event_id)
                    try:
                        bot.deleteMessage((msgs_id, get_event(event_id)['event_msg_id']))
                    except:
                        pass
                    conn.execute(query)
                    conn.commit()
                    bot.sendMessage(chat_id, "❎رویداد مورد نظر حذف شد")
                    show_main_keyboard(user_data, msg)
            if (msg['text'].startswith("/start rem_")):
                if (user_data['is_admin'] == 0):
                    tmp = chat_id
                    chat_id = get_user_data(chat_id)['id']
                    event_id = msg['text'][11:]
                    conn = sqlite3.connect(db_name)
                    query = "update events set sign_ups = ? where id=" + str(event_id)
                    sign_ups = get_sign_ups(event_id)
                    if (not str(chat_id) in sign_ups):
                        bot.sendMessage(chat_id,
                                        "شما در رویداد مورد نظر شرکت نکرده اید , برای ترک یک رویداد باید ابتدا در آن ثبت نام کنید")
                        return
                    new_sign_ups = ""
                    for i in range(len(sign_ups.split(','))):
                        if (not str(chat_id) in sign_ups.split(',')[i]):
                            new_sign_ups += sign_ups.split(',')[i] + ","
                    conn.execute(query, [new_sign_ups])
                    conn.commit()
                    chat_id = tmp
                    bot.sendMessage(chat_id, "❎شما رویداد مورد نظر را ترک کردید.", reply_markup=states[2])
                    return
                if (user_data['is_admin'] == 1):
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
                    bot.sendMessage(chat_id, "❎رویداد مورد نظر حذف شد")
                    show_main_keyboard(user_data, msg)

            if (msg['text'].startswith("/start show_")):
                try:
                    event_msg_id = msg['text'][12:]
                    bot.forwardMessage(chat_id, msgs_id, event_msg_id)
                    show_main_keyboard(user_data, msg)
                except:
                    bot.sendMessage(chat_id, "یافت نشد")
            if (msg['text'].startswith("/start show2_")):
                try:
                    event_msg_id = msg['text'][13:]
                    bot.forwardMessage(chat_id, msgs_id, event_msg_id)
                    show_main_keyboard(user_data, msg)
                except:
                    bot.sendMessage(chat_id, "یافت نشد")

            if ("خروج" in msg['text']):

                set_state(chat_id, "ask_exit")
                bot.sendMessage(chat_id, "آیا قصد خروج از حساب خود را دارید ؟", reply_to_message_id=msg['message_id'],
                                reply_markup=states[4])
                return
            if (msg['text'] == 'ℹ️مشخصاتℹ️'):
                bot.sendMessage(chat_id, get_info(chat_id, user_data), parse_mode="markdown",
                                reply_to_message_id=msg['message_id'])
                return
            if (msg['text'] == '➕ثبت رویداد عمومی➕'):
                set_state(chat_id, "event2start")
                bot.sendMessage(chat_id, "لطفا نام رویداد مورد نظر انتخاب کنید", reply_markup=states[1])
            if (msg['text'] == '📭پشتیبانی📭'):
                set_state(chat_id, "talking")
                txxt = """شما در ارتباط با پشتیبانی هستید , لطفا پیام خود را ارسال نمایید , پشتیبانی در اسرع وقت به آن پاسخ خواهد داد.
"""
                bot.sendMessage(chat_id, txxt, reply_markup=states[1])
                return
            if (msg['text'] == "مشاوره"):
                bot.sendMessage(chat_id , "لطفا نوع مشاوره خود را انتخاب کنید."  , reply_markup=states[10])
                set_state(chat_id , "MOSHAVERETYPE")
                return
            if(msg['text'] == "ویرایش اطلاعات️"):
                Userhandle.set_column("users","melli_code" , chat_id , "")
                Userhandle.set_column("users" , "phno" , chat_id , "")
                show_main_keyboard(user_data,msg)

            if (msg['text'] == "🖊عضویت در رویداد🖊"):
                conn = sqlite3.connect(db_name)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                query = "select event_name,id,sign_ups,event_type from events"
                curs = conn.execute(query)
                tmp = chat_id
                chat_id = get_user_data(chat_id)['id']
                for row in curs:
                    if (not str(chat_id) in row[2]):
                        keyboard.inline_keyboard.append(
                            [InlineKeyboardButton(text=row[3] + "-" + row[0], callback_data="event_" + str(row[1]))])
                chat_id = tmp
                if (len(keyboard.inline_keyboard) != 0):
                    bot.sendMessage(chat_id, "لطفا رویداد مورد نظر خود را از لیست پایین انتخاب نمایید",
                                    reply_markup=states[1])
                    bot.sendMessage(chat_id, "🎈رویداد ها🎈", reply_markup=keyboard)
                    set_state(chat_id, "choosing_event")
                else:
                    bot.sendMessage(chat_id, "❌رویدادی یافت نشد")
            if (msg['text'] == '🗂رویداد های عضو شده🗂'):
                conn = sqlite3.connect(db_name)
                query = "select event_name,id,event_msg_id,event_type from events where sign_ups like '%" + str(
                    get_user_data(chat_id)['id']) + "%' ORDER BY event_type ASC limit 70 "
                curs = conn.execute(query)
                matn = "رویداد های ثبت نام شده :" + "\n"
                lol = -1
                for row in curs:
                    if (row[3] == "آموزشی" and lol == -1):
                        matn += "آموزشی : \n"
                        lol = 0
                    if (row[3] == "رفاهی" and lol == 0):
                        matn += "رفاهی :\n"
                        lol = 1
                    if (row[3] == "سایر" and lol == 1):
                        matn += "سایر : \n"
                        lol = 2

                    matn += row[0] + " : " + "[" + " حذف رویداد" + "](https://telegram.me/BengC_bot?start=rem_" + str(
                        row[1]) + ") | [" + "مشاهده" + "](https://telegram.me/BengC_bot?start=show_" + str(
                        row[2]) + ")\n"
                if (matn == "رویداد های ثبت نام شده :" + "\n"):
                    bot.sendMessage(chat_id, "شما در رویدادی ثبت نام نکرده اید")
                    return
                else:
                    bot.sendMessage(chat_id, matn, parse_mode="markdown")
                    return

            if (msg['text'] == "➕ثبت رویداد➕" and user_data['is_admin'] == 1):
                set_state(chat_id, "choosing_eventtype")
                bot.sendMessage(chat_id, "لطفا نوع رویداد را مشخص کنید : ", reply_markup=states[7])
                return

            if (msg['text'] == "📄افزودن دستی📄" and user_data['is_admin'] == 1):
                set_state(chat_id, "afzudan")
                bot.sendDocument(chat_id, open("input.xlsx", "rb"), caption="فایل قالب")
                bot.sendMessage(chat_id,
                                "لطفا فایل قالب را دانلود کرده و اطلاعات افراد جدید را در آن ثبت نمایید و آپلود کنید. دقت به نکات زیر اهمیت دارد :" + "\n\n" + "۱-اگر قسمت کد عضویت را خالی بگذارید ؛ توسط ربات به آن شخص آیدی داده میشود و در انتها آیدی آن شخص فرستاده میشود و اگر قسمت کد عضویت یک شخص را پر کنید؛ در صورتی که آن کد عضویت در دیتابیس موجود باشد؛ آن شخص اضافه نشده و در انتها در لیست ارور ها چاپ میشود." + "\n\n" + "۲-تمامی فیلد ها بجز قسمت نام و نام خانوادگی میتوانند خالی بمانند و اگر برای شخصی نام و نام خانوادگی مشخص نشود ؛ اضافه نخواهد شد و در انتها در لیست ارور ها چاپ میشود." + "\n\n" + "۳-دقت کنید که ربات تنها در صورتی جلوی عضویت دو شخص با نام یکسان را میگیرد که آیدیشان یکسان باشد. پس مراقب عضو نمودن تکراری افراد باشید؛ برای مثال دو نفر با نام 'علی رضایی' و 'علی رضایی' و با آیدی های مختلف ؛ متفاوت شناخته میشوند و امکان ثبت دوباره یک شخص وجود دارد؛ برای جلوگیری از این امر ابتدا از عدم عضویت اشخاص اطمینان حاصل فرمایید",
                                reply_markup=states[1])
                return
            if (msg['text'] == "📌پیام همگانی📌" and user_data['is_admin'] == 1):
                set_state(chat_id, "sending_msgall")
                bot.sendMessage(chat_id, "لطفا پیام خود را ارسال کنید", reply_markup=states[1])
                return
            if (msg['text'] == "📌پیام گروهی📌" and user_data['is_admin'] == 1):
                set_state(chat_id, "sending_msgone")
                bot.sendMessage(chat_id, "لطفا پیام خود را ارسال کنید", reply_markup=states[1])
            if (msg['text'] == '🗃پشتیبان🗃' and user_data['is_admin'] == 1):
                bot.sendDocument(chat_id, open("usersdb.db", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Excel_Handler.py", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Userhandle.py", 'rb'), reply_to_message_id=msg['message_id'])
                bot.sendDocument(chat_id, open("Bot.py", 'rb'), reply_to_message_id=msg['message_id'])
                return
            if (msg['text'] == '📑مدیریت رویدادها📑' and user_data['is_admin'] == 1):
                text = ""
                conn = sqlite3.connect(db_name)
                query = "select event_name,id,event_msg_id,event_type from events order by event_type limit 300"
                curs = conn.execute(query)
                matn = "لیست رویداد ها : " + "\n"
                lol = -1
                for row in curs:
                    if (row[3] == "آموزشی" and lol == -1):
                        matn += "آموزشی : \n"
                        lol = 0
                    if (row[3] == "رفاهی" and lol == 0):
                        matn += "رفاهی :\n"
                        lol = 1
                    if (row[3] == "سایر" and lol == 1):
                        matn += "سایر : \n"
                        lol = 2

                    event = get_event(row[1])
                    matn += row[0] + " (" + str(len([k for k in event['sign_ups'].split(',') if str.isnumeric(
                        k)])) + ") : " + "[" + " حذف رویداد" + "](https://telegram.me/BengC_bot?start=rem_" + str(
                        row[1]) + ") | [" + "مشاهده" + "](https://telegram.me/BengC_bot?start=show_" + str(
                        row[2]) + ")\n"
                matn += "\n\n" + "رویداد های عمومی : " + "\n"
                query = "select name,id,msgid from events2"
                curs = conn.execute(query)
                for row in curs:
                    event = get_event2(row[1])
                    matn += row[0] + " : " + "[" + " حذف رویداد" + "](https://telegram.me/BengC_bot?start=rem2_" + str(
                        row[1]) + ") | [" + "مشاهده" + "](https://telegram.me/BengC_bot?start=show2_" + str(
                        row[2]) + ")\n"
                if (matn == "لیست رویداد ها : " + "\n"):
                    bot.sendMessage(chat_id, "رویدادی وجود ندارد")
                    return
                else:
                    bot.sendMessage(chat_id, matn, parse_mode="markdown")
                    return
            if (msg['text'] == '📊گزارش گیری📊' and user_data['is_admin'] == 1):
                set_state(chat_id, "sta_select")
                bot.sendMessage(chat_id, "❗️لطفا بخش مورد نظر خود را انتخاب نمایید",
                                reply_to_message_id=msg['message_id'], reply_markup=states[5])


def on_callback_query(msg):
    query_id, from_id, query_data = telepothelli.glance(msg, flavor='callback_query')
    print(msg)
    # print(query_data)
    if (query_data.startswith("1reshte_") and get_user_state(from_id) == "ask_reshte"):
        num = query_data.replace("1reshte_", "")
        kk = ["معماری", "برق", "مکانیک", "نقشه برداری", "ترافیک", "عمران", "سایر"]
        reshte = kk[int(num) - 1]
        chat_id = from_id
        set_column('users', 'reshte', from_id, reshte)
        set_state(chat_id, "main")
        user_data = get_user_data(chat_id)
        show_main_keyboard(user_data, msg)
       # if (reshte == "سایر"):
       #     set_state(chat_id, "main")
       #     user_data = get_user_data(chat_id)
       #     show_main_keyboard(user_data, msg)
       # else:
       #     set_state(chat_id, "1Dask")
       #     keyboard = keyboard = InlineKeyboardMarkup(inline_keyboard=[
       #         [InlineKeyboardButton(text='✅بله✅', callback_data="1yep"),
       #          InlineKeyboardButton(text='❌خیر❌', callback_data="1Nop")]])
       #     bot.sendMessage(chat_id, "آیا دانشجویی مقطع کارشناسی هستید ؟", reply_markup=keyboard)
        return
    if (query_data == "1yep" and get_user_state(from_id) == "1Dask"):
        chat_id = from_id
        set_column('users', 'ozviat_type', chat_id, "دانشجویی")
        set_state(chat_id, "main")
        user_data = get_user_data(chat_id)
        show_main_keyboard(user_data, msg)
        return
    if (query_data == "1Nop" and get_user_state(from_id) == "1Dask"):
        chat_id = from_id
        set_column('users', 'ozviat_type', chat_id, "پیوسته")
        set_state(chat_id, "main")
        user_data = get_user_data(chat_id)
        show_main_keyboard(user_data, msg)
        return
    if(query_data.startswith("OMRAN_")):
        chat_ID = query_data.replace("OMRAN_" , "")
        bot.sendDocument(chat_ID , open("cart1_"+chat_ID+".png" , "rb"), "#عمران")
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        return
    if(query_data.startswith("SAKHTEMAN_")):
        chat_ID = query_data.replace("SAKHTEMAN_", "")
        bot.sendDocument(chat_ID, open("cart2_" + chat_ID + ".png", "rb"), "#ساختمان")
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        return
    if (query_data.startswith("reshte_") and get_user_state(from_id) == "reshte_choosing"):
        num = query_data.replace("reshte_", "")
        kk = ["معماری", "برق", "مکانیک", "نقشه برداری", "ترافیک", "عمران", "سایر"]
        reshte = kk[int(num) - 1]
        chat_id = from_id
        save_data(chat_id, "reshte", reshte)
        if (reshte == "سایر"):
            if(load_data(chat_id , "ozviat_type") != "دانشجویی"):
                save_data(chat_id, "ozviat_type", "مهمان")
            set_state(chat_id, 'sending_profile_pic')
        else:
            if (load_data(chat_id, "ozviat_type") != "دانشجویی"):
                save_data(chat_id, "ozviat_type", "پیوسته")
            set_state(chat_id, 'sending_profile_pic')
        bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        #    set_state(chat_id, "Dask")
        #    keyboard = keyboard = InlineKeyboardMarkup(inline_keyboard=[
        #        [InlineKeyboardButton(text='✅بله✅', callback_data="yep"),
        #         InlineKeyboardButton(text='❌خیر❌', callback_data="Nop")]])
        #    bot.sendMessage(chat_id, "آیا دانشجویی مقطع کارشناسی هستید ؟", reply_markup=keyboard)
        return

    if (query_data == "yep" and get_user_state(from_id) == "Dask"):
        chat_id = from_id
        save_data(from_id, "ozviat_type", "دانشجویی")
        set_state(chat_id, 'sending_profile_pic')
        bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        return
    if (query_data == "Nop" and get_user_state(from_id) == "Dask"):
        chat_id = from_id
        save_data(from_id, "ozviat_type", "پیوسته")
        set_state(chat_id, 'sending_profile_pic')
        bot.sendMessage(chat_id, "✅لطفا عکس پرسنلی خود را ارسال کنید.")
        return
    if (query_data.startswith("ye2s_")):
        r_id = query_data.split("_")[1]
        event_id = query_data.split("_")[2]
        register_event2(event_id, r_id)
        user = get_user_by_id(r_id)
        try:
            bot.sendMessage(user['tcode'], "✅در رویداد مورد نظر با موفقیت عضو شدید.")
        except:
            pass
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        pass
    elif (query_data.startswith("n2o_")):
        r_id = query_data.split("_")[1]
        event_id = query_data.split("_")[2]
        user = get_user_by_id(r_id)
        try:
            bot.sendMessage(user['tcode'],
                            "در رویداد مورد نظر ثبت نشدید! اگر فکر میکنید مشکلی پیش آمده با ادمین یا پشتیبانی تماس حاصل فرمایید.")
        except:
            pass
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    if (query_data.startswith("yes_")):
        chat_id = query_data.split('_')[1]
        # do some shit here
        bot.sendMessage(chat_id, "عضویت شما تایید شد.")

        set_state(chat_id, "entering_name2")
        bot.sendMessage(chat_id, "لطفا نام کامل خود را وارد نمایید (نام و نام خانوادگی)",
                        reply_markup=ReplyKeyboardRemove())
        bot.sendPhoto(pics_backup, msg['message']['photo'][-1]['file_id'], caption=chat_id)
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    elif (query_data.startswith("no_")):
        chat_id = query_data.split("_")[1]
        bot.sendMessage(chat_id,
                        "فیش شما مورد پذیرش قرار نگرفت , لطفا در صورت اطمینان با پشتیبانی یا ادمین تماس حاصل فرمایید")
        set_state(chat_id, "login")
        bot.sendMessage(chat_id, "لطفا گزینه خود را انتخاب کنید", reply_markup=states[0])
        bot.deleteMessage(telepothelli.origin_identifier(msg))

    if(query_data.startswith("yems_")):
        chat_id = query_data.split("_")[1]
        t = "لطفا مبلغ 200,000 تومان را به شماره حساب :\n" + "5022 2913 0240 6226\n" + "به نام محمد شریفی(امور مالی) واریز نموده و تصویر رسید واریزی را ارسال نمایید."
        bot.sendMessage(chat_id , ("کارت دانشجویی شما مورد قبول قرار گرفت. " +"\n"+t))
        set_state(chat_id, "sending_fish")
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    elif(query_data.startswith("nmo_")):
        chat_id = query_data.split("_")[1]
        bot.sendMessage(chat_id,
                        "کارت شما مورد پذیرش قرار نگرفت , لطفا در صورت اطمینان با پشتیبانی یا ادمین تماس حاصل فرمایید")
        set_state(chat_id, "login")
        bot.sendMessage(chat_id, "لطفا گزینه خود را انتخاب کنید", reply_markup=states[0])
        bot.deleteMessage(telepothelli.origin_identifier(msg))
    if (query_data.startswith("event_")):
        # dar asl baya in bashe ke aval bebinan rooydad haro bad azashoon beporse ke aya mikhayd ozv beshid ya na vali in movaghatie
        event_id = query_data.split('_')[1]
        event = get_event(event_id)
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        try:
            bot.forwardMessage(from_id, msgs_id, event['event_msg_id'])
        except:
            bot.sendMessage(from_id, "محتوای رویداد مورد نظر حذف شده!")
        #if (event['event_type'] != 'رفاهی'):
        set_state(from_id, "event_yon")
        save_data(from_id, "event_id", event_id)
        bot.sendMessage(from_id, "آیا مایلید در رویداد بالا ثبت نام کنید ؟", reply_markup=states[4])
    if (query_data.startswith("event2_")):
        event_id = query_data.split('_')[1]
        event = get_event2(event_id)
        bot.deleteMessage(telepothelli.origin_identifier(msg))
        set_state(from_id, "event2_yon")
        save_data(from_id, "event2_id", event_id)
        try:
            bot.forwardMessage(from_id, msgs_id, event['msgid'])
        except:
            bot.sendMessage(from_id, "محتوای رویداد مورد نظر حذف شده!")
        bot.sendMessage(from_id, "آیا مایلید در رویداد بالا ثبت نام کنید ؟", reply_markup=states[4])


def register_event(event_id, from_id):
    sign_ups = get_sign_ups(event_id)
    if (sign_ups == "" or sign_ups == None):
        sign_ups += str(get_user_data(from_id)['id'])
    else:
        sign_ups += "," + str(get_user_data(from_id)['id'])
    conn = sqlite3.connect(db_name)
    query = "update events set sign_ups = ? where id = ?"
    conn.execute(query, [sign_ups, int(event_id)])
    conn.commit()

def register_eventS(event_id, from_id , name , melliCode):
    sign_ups = get_sign_ups(event_id)
    if (sign_ups == "" or sign_ups == None):
        sign_ups += str(get_user_data(from_id)['id'])+"$"+name+"$"+melliCode
    else:
        sign_ups += "," + str(get_user_data(from_id)['id'])+"$"+name+"$"+melliCode
    conn = sqlite3.connect(db_name)
    query = "update events set sign_ups = ? where id = ?"
    conn.execute(query, [sign_ups, int(event_id)])
    conn.commit()



def register_event2(event_id, id):
    sign_ups = get_sign_ups(event_id)
    if (sign_ups == "" or sign_ups == None):
        sign_ups += str(get_user_data(from_id)['id'])
    else:
        sign_ups += "," + str(id)
    conn = sqlite3.connect(db_name)
    query = "update events set sign_ups = ? where id = ?"
    conn.execute(query, [sign_ups, int(event_id)])
    conn.commit()


def register_event3(chat_id, event_id, phone, name):
    sign_ups = get_sign_ups2(event_id)
    if (sign_ups == "" or sign_ups == None):
        sign_ups = ""
        sign_ups += str(chat_id) + ":" + str(name) + ":" + str(phone)
    else:
        sign_ups += "," + str(chat_id) + ":" + str(name) + ":" + str(phone)
    conn = sqlite3.connect(db_name)
    query = "update events2 set signedtcodes = ? where id = ?"
    conn.execute(query, [sign_ups, int(event_id)])
    conn.commit()


token = ""

bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)

