import openpyxl
import re


def readTable(filename,columns):
    wb_obj = openpyxl.load_workbook(filename) #get a excel object
    sheet_obj = wb_obj.active #get it's main sheet
    if(columns==[]): #if column addresses were empty then what we want to read ?
        return []
    data = [] # the thing we want to return , each row is a dict (json format)
    col_names =[] #it stores the alphabatic part of each column (AD12 => AD)
    col = [] #it stores the name of column : id , name , etc
    for column in columns:
        col_names.append("")
        for i in range(len(column)):
            if(not str.isdigit(column[i])): #we add the alphabatic part till it is alphabatic
                col_names[-1]+=column[i]
        if(sheet_obj[column].value == None):
            return []
        col.append(sheet_obj[column].value) #column names
    i=int(re.search(r'\d+', columns[0]).group()) + 1 #get the int part of the column address , A12 => 12
    while(True):
        if(sheet_obj[col_names[0]+str(i)].value == None): #when we reached to the end of the table
            break
        dat = dict()
        for j in range(len(col)):
            dat[col[j]] = sheet_obj[col_names[j]+str(i)].value
        data.append(dat)
        i+=1
    return data

def writeTable(columnnames , columns_addr , rows , filename):
    wb = openpyxl.Workbook()
    sheet = wb.active
    if(len(columnnames)!=len(columns_addr)):
        return False
    # Set the column names in the excel file
    for i in range(len(columnnames)):
        sheet[columns_addr[i]].value = columnnames[i]
    col_addr = [] #the alphabatic part of column addresses
    for i in range(len(columns_addr)):
        adr = ""
        for j in range(len(columns_addr[i])):
            if(not str.isdigit(columns_addr[i][j])):
                adr+=columns_addr[i][j]
        col_addr.append(adr)
    i = int(re.search(r'\d+', columns_addr[0]).group()) + 1  # get the int part of the column address , A12 => 12
    #now it's time to put the rows in the excel file
    for row in rows:
        for j in range(len(col_addr)):
            sheet[col_addr[j]+str(i)].value = row[j]
        i+=1
    wb.save(filename) #save it to excel file
