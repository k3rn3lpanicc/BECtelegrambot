import sqlite3
import codecs
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
    value = ""
    for row in curs:
        value = row[0]
    if(value == '' or value == None):
        return ""
    return value

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