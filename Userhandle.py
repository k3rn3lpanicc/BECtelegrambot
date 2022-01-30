import sqlite3
import codecs
import json

taeed_channel = "-1001770860875"
db_name = "usersdb.db"
pics_backup = "-1001594222928"
msgs_id = "-1001737741022"
def get_user_cr(telegram_id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute("select * from users2 WHERE tid = ?",[str(telegram_id)])
    rows = []
    for row in curs:
        rows.append(row)
    return rows

def get_value(tablename , telegram_id , column_name):
    va = "tcode" if tablename == 'users' else "tid"
    conn = sqlite3.connect(db_name)
    query = "SELECT "+column_name+" FROM " + tablename + " WHERE "+va+" = ?"
    curs = conn.execute(query , [str(telegram_id)])
    for row in curs:
        return str(row[0])
    return ""

def is_name_valid(telegram_id , name ,  code):
    names = []
    conn =sqlite3.connect(db_name)
    query = "select name from users where id = ?"
    curs = conn.execute(query , [str(code)])
    for row in curs:
        names.append(row[0])
    if(len(names)==0):
        return False
    if(name in names):
        return name
    else:
        for na in names:
            if(valid(name , na)):
                return na
        return False
def valid(sm , la):
    ret = False
    sm2 = sm.split(" ")
    la2 = la.split(" ")
    cnt  = 0
    for word in sm2:
        if(word in la2):
            cnt+=1
    if(cnt>=2):
        return True
    return False

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
        rr['photo_id'] = row[5]
        rr['is_admin'] = row[6]
        rr['last_login_date'] = row[7]
        rr['last_activity_date'] = row[8]
        rr['melli_code'] = row[9]
        rr['reshte'] = row[10]
        rr['ozviat_type'] = row[11]
        return rr
    return False
def get_user_data_by_id(id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute('SELECT * FROM users WHERE id = ?' , [str(id)])
    rr = dict()
    for row in curs:
        rr['uid'] = row[0]
        rr['id'] = row[1]
        rr['name'] = row[2]
        rr['tcode'] = row[3]
        rr['phno'] = row[4]
        rr['photo_id'] = row[5]
        rr['is_admin'] = row[6]
        rr['last_login_date'] = row[7]
        rr['last_activity_date'] = row[8]
        rr['melli_code'] = row[9]
        rr['reshte'] = row[10]
        rr['ozviat_type'] = row[11]
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
    conn.execute("insert into users2 values(?,?,?,?)",[str(telegram_id),"-1","",""])
    conn.commit()
def set_column(table_name , column_name , telegram_id,value):
    conn = sqlite3.connect(db_name)
    va = "tid"
    if(table_name == 'users'):
        va = 'tcode'
    query = "UPDATE "+table_name +" SET "+column_name +" = ? WHERE "+va+" = ?"
    print(query)
    conn.execute(query , [str(value) , str(telegram_id)])
    conn.commit()


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
#def appendtodatabas(excelfilename , columns):
#    data = Excel_Handler.readTable(excelfilename,columns)
#    conn = sqlite3.connect(db_name)
#   for row in data:
#        conn.execute("INSERT into users(id,name) values(?,?)" , [row['id'],row['name']])
#    conn.commit()
def check_name(name):
    for ch in list(name):
        if((not str.isalpha(ch)) and ch!=' '):
            return False
        if((ord(ch)>= ord('a') and ord(ch)<= ord('z')) or (ord(ch)>= ord('A') and ord(ch)<= ord('Z'))):
            return False
    return True

def save_data(chat_id , keyname , value):
    current_data = get_value('users2',chat_id,'data')
    if(current_data==""):
        set_column('users2',"data",chat_id,"{}")
        save_data(chat_id , keyname , value)
    else:
        data = json.loads(current_data)
        data[keyname] = value
        set_column('users2' , 'data',chat_id , json.dumps(data))

def load_data(chat_id , keyname):
    data = json.loads(get_value('users2' ,chat_id,'data'))
    if(keyname in data):
        return data[keyname]
    else:
        return False

def remove_data(chat_id , keyname):
    data = json.loads(get_value('users2' ,chat_id,'data'))
    if(keyname in data):
        del(data[keyname])
        set_column('users2' ,'data' , chat_id, json.dumps(data))
        return True
    return False
def register_code(reshte):

    conn = sqlite3.connect(db_name)
    query = ""
    if(reshte == "عمران"):
        query = 'select Max(id) from users where users.id like "300%"'
    else:
        query = 'select Max(id) from users where users.id like "600%"'
    curs = conn.execute(query)
    id = ""
    for row in curs:
        id = str(int(row[0])+1)
    if(id == None):
        id = ""
    return id

def insert_users(id , name , chat_id , phno):
    conn = sqlite3.connect(db_name)
    query = "INSERT INTO users(id , name , tcode , phno) values(? , ? , ? , ?)"
    conn.execute(query , [str(id) , str(name) , str(chat_id) , str(phno)])
    conn.commit()
def get_chat_id(id):
    conn = sqlite3.connect(db_name)
    query = "Select tcode from users where id = ?"
    curs = conn.execute(query , [str(id)])
    for row in curs:
        return  row[0]
    return ""
def get_user_by_id(id):
    conn = sqlite3.connect(db_name)
    query = "SELECT * from users WHERE id = ?"
    curs = conn.execute(query, [str(id)])
    rr = dict()
    for row in curs:
        rr['uid'] = row[0]
        rr['id'] = row[1]
        rr['name'] = row[2]
        rr['tcode'] = row[3]
        rr['phno'] = row[4]
        rr['photo_id'] = row[5]
        rr['is_admin'] = row[6]
        rr['last_login_date'] = row[7]
        rr['last_activity_date'] = row[8]
        rr['melli_code'] = row[9]
        rr['reshte'] = row[10]
        rr['ozviat_type'] = row[11]
        return rr
    return False

def send_to_all(bot,txt):
    conn = sqlite3.connect(db_name)
    query = "select tcode from users where (tcode is not null and tcode is not '')"
    curs = conn.execute(query)
    for row in curs:
        bot.sendMessage(row[0],txt)
def send_to_all_2(bot,chat_id,msg_id):
    conn = sqlite3.connect(db_name)
    query = "select tcode from users where (tcode is not null and tcode is not '')"
    curs = conn.execute(query)
    for row in curs:
        bot.forwardMessage(row[0], chat_id, msg_id)
def get_sign_ups(id):
    conn = sqlite3.connect(db_name)
    query = "select sign_ups from events where id = ?"
    curs = conn.execute(query , [int(id)])
    for row in curs:
        return row[0]

def get_event_name(id):
    conn = sqlite3.connect(db_name)
    query = "select event_name from events where id = ?"
    curs = conn.execute(query, [int(id)])
    for row in curs:
        return row[0]

def get_info(chat_id , user_data):
    return "نام و نام خانوادگی : " +"`"+ user_data['name'] +"`\nکد عضویت : " +"`" + user_data['id']+ "`\nشماره همراه : " +"`" + str(user_data['phno']+"`\nکد ملی :"+"`" + (user_data['melli_code'])+"`\nنقش : "+"`"+("ادمین" if user_data['is_admin']==1 else "کاربر")+"`")

def insert_event(event_name , event_msg_id):
    conn = sqlite3.connect(db_name)
    query = "insert into events (event_name , event_msg_id) Values (? , ?)"
    conn.execute(query , [str(event_name) , str(event_msg_id)])
    conn.commit()

def get_event(id):
    conn = sqlite3.connect(db_name)
    query = "select * from events where id = ?"
    curs = conn.execute(query, [str(id)])
    rr = dict()
    for row in curs :
        rr['id'] = row[0]
        rr['event_name'] = row[1]
        rr['event_msg_id'] = row[2]
        rr['sign_ups'] = row[3]
        return rr
def get_activitys(id):
    conn = sqlite3.connect(db_name)
    query = "select event_name from events where sign_ups like '%"+str(get_user_data(id)['id'])+"%'"
    curs = conn.execute(query)
    mtn = ""
    for row in curs:
        mtn+="`"+row[0]+"`\n"
    return mtn

def get_all_events():
    conn = sqlite3.connect(db_name)
    query = "Select * from events"
    rows = []
    curs = conn.execute(query)
    for row in curs:
        b = dict()
        b['id'] = row[0]
        b['event_name'] = row[1]
        b['sign_ups'] = row[3]
        rows.append(b)
    return rows if len(rows)!=0 else False

def get_admins():
    ret = "لیست ادمین ها : \n" + "\n "
    conn = sqlite3.connect(db_name)
    query = "select id,name,phno,melli_code from users where is_admin = ?"
    curs = conn.execute(query, [1])
    for row in curs:
        ret += "نام و نام خانوادگی : " +"`" + str(row[1])+"`\n "+ "کد عضویت : " + "`"+  str(row[0])+ "`\n " + "شماره تماس : "+"`"+ str(row[2])+"`\n "+"کد ملی : "+ "`"+ row[3]+"`\n\n"
    return ret

def get_melli_code_by_chat_id(chat_id):
    conn = sqlite3.connect(db_name)
    query = "select melli_code from users where tcode = ?"
    curs = conn.execute(query, [str(chat_id)])
    for row in curs:
        if(row[0]!="-"):
            return row[0]
    return "-"
def get_melli_code_by_id(id):
    conn = sqlite3.connect(db_name)
    query = "select melli_code from users where id = ?"
    curs = conn.execute(query, [str(id)])
    for row in curs:
        if (row[0] != "-"):
            return row[0]
    return "-"

def is_melli_valid(melli):
    ans = 0
    for i in range(len(melli)):
        ans+= (i+1)*int(melli[i])
    if(ans%11 == 0):
        return True
    return False


def is_phone_valid(ph):
    if(len(ph)>12 or len(ph)<10):
        return False
    if(ph[0] not in ['0' , '9']):
        return False
    return True