import sqlite3
import codecs

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
