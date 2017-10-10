import sqlite3
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import datetime
from datetime import datetime, timedelta
import os
import shutil

databaseName = 'last_check.sqlite'
#make table
def datetime_tbl():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS datetime_tbl(datestamp TEXT)');
    c.close()
    conn.close()
#grab entry from ui
def data_entry():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute("INSERT INTO datetime_tbl (datestamp) VALUES (?)", (str(datetime.now()),))
    conn.commit()
    conn.close()

#this grabs file transfer from tbl for entry form              
def generatelasttransfer():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    global transfer
    transfer = c.execute("""SELECT MAX(datestamp) FROM datetime_tbl ORDER BY datestamp DESC LIMIT 1""").fetchall() 
    #print(transfer)#testing
    return(transfer)
    c.close()
    #conn.close()    
    
def ui(root):
    '''
    #transfer = str()
    transfer = StringVar()
    transfer.set(generatelasttransfer())
    src_filename = str()
    des_filename = str()
    '''
    transfer = StringVar()
    transfer.set(generatelasttransfer())
    src_filename = StringVar()
    #src_filename.set(src_files())
    des_filename = StringVar()
    #des_filename.set(des_files())
    

    #btn for main file transfer 
    btn_ck = tk.Button(
    text='File Transfer',
    command=f_transfer(src_filename, des_filename)).grid(row=7, column=2, padx=5, pady=5)
    #btns for src and des files
    btn_src = tk.Button(text='Choose file to send out',command=get_file(src_filename)).grid(row=2, column=2, padx=5, pady=5)
    btn_des = tk.Button(text='Choose file to send to',command=get_file(des_filename)).grid(row=2, column=4, padx=5, pady=5)
    # btn for generatelasttransfer
    #btn_func = tk.Button(text='Last Transfer',command= generatelasttransfer).grid(row = 3, column = 4, padx = 3, pady = 3)
    
    tk.Entry(text= src_filename).grid(row = 3, column = 2, padx = 15, pady = 5)
    tk.Entry(text= des_filename).grid(row = 3, column = 4, padx = 15, pady = 5)
    tk.Entry(root, textvariable = transfer, width=28).grid(row = 7,column = 4,padx = 7,pady = 7)

        
def get_file(src_filename):
    def wrap():
        src_filename.set(filedialog.askdirectory())
    return wrap1
def get_file(des_filename):
    def wrap():
        des_filename.set(filedialog.askdirectory())
    return wrap
#file transfer
def f_transfer(src_filename, des_filename):
    def wrap():
        _src_filename, _des_filename = src_filename.get(), des_filename.get()
        for root,dirs,files in os.walk(_src_filename):
            for file_name in files:
                now = datetime.now()
                before = now - timedelta(hours=24)
                files = os.path.join(_src_filename, file_name)
                mod_time = datetime.fromtimestamp(os.path.getmtime(files))
                if mod_time > before:
                    shutil.move(
                        os.path.join(_src_filename, file_name), 
                        _des_filename
                    )
                    data_entry()
    return wrap
#

if __name__ == '__main__':
    datetime_tbl()
    root = Tk()
    ui(root)
    root.mainloop
