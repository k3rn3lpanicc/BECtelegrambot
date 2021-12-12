import sqlite3
import codecs
import json

taeed_channel = "-1001770860875"
db_name = "usersdb.db"
def get_user_cr(telegram_id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute("select * from users2 WHERE tid = ?",[str(telegram_id)])
    rows = []
    for row in curs:
        rows.append(row)
    return rows

def get_value(tablename , telegram_id , column_name):
    conn = sqlite3.connect(db_name)
    query = "SELECT "+column_name+" FROM " + tablename + " WHERE tid = ?"
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
    curs = conn.execute('SELECT * FROM users WHERE tcode = ? Limit 1' , [str(telegram_id)])
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
    conn.execute("insert into users2 values(?,?,?,?)",[str(telegram_id),"-1","",""])
    conn.commit()
def set_column(table_name , column_name , telegram_id,value):
    conn = sqlite3.connect(db_name)
    va = "tid"
    if(table_name == 'users'):
        va = 'tcode'
    query = "UPDATE "+table_name +" SET "+column_name +" = ? WHERE "+va+" = ?"
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
def appendtodatabas(excelfilename , columns):
    data = Excel_Handler.readTable(excelfilename,columns)
    conn = sqlite3.connect(db_name)
    for row in data:
        conn.execute("INSERT into users(id,name) values(?,?)" , [row['id'],row['name']])
    conn.commit()
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
def register_code():
    conn = sqlite3.connect(db_name)
    query = "select MAX(id) from users"
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
    query = "Select tid from users2 where id = ?"
    curs = conn.execute(query , [str(id)])
    for row in curs:
        return  row[0]
    return ""