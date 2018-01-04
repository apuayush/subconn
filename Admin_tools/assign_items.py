from pymongo import MongoClient
from config import var
import json
import sys
import requests
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

client = MongoClient(var.link)
db = client['subconn']

rice = 0
wheat = 0
sugar = 0
oil = 0
def check():
    global rice, wheat, sugar, oil
    rice = db.items.find({"name": "Rice", "assigned_to": "Factory"}).count()
    wheat = db.items.find({"name": "Wheat", "assigned_to": "Factory"}).count()
    sugar = db.items.find({"name": "Sugar", "assigned_to": "Factory"}).count()
    oil = db.items.find({"name": "Oil", "assigned_to": "Factory"}).count()
    blank1.insert(0, rice)
    blank2.insert(0, wheat)
    blank3.insert(0, sugar)
    blank4.insert(0, oil)

def update_count(uname, r, w, s, o, each):
    db.agent_details.update({"uid": uname}, {'$set': \
                                                 {"item_count": {"Rice": each["Rice"] + r, "Wheat": each["Wheat"] + w,
                                                                 "Sugar": each["Sugar"] + s, "Oil": each["Oil"] + o}}})

def mark(uid, typ, quan):
    for each in db.items.find({"name": typ, "assigned_to": "Factory"}):
        if not quan:
            break
        data = {
            "from": "Factory",
            "to": uid,
            "jwt": "1234567890",
            'gps': "",
            'prev_trans': "None"
        }
        tid = requests.post("http://35.200.142.66:8080/transaction",
                            data=data).json()
        print(tid)

        db.items.update({"code": each["code"]}, {'$set': {"assigned_to": uid, "transaction_id": tid['transactionHash']}})
        quan -= 1

def is_number(s, val):
    try:
        int(s)
        ret = int(s)
        if val-ret>=0:
            return int(s)
        return 0
    except ValueError:
        return 0

def assign():
    uname = int(name.get())
    if db.agent_details.find({"uid": uname}).count() == 1:
        each = db.agent_details.find({"uid": uname})[0]
        uid = each["uid"]
        each = each["item_count"]
        r = is_number(rb.get(), rice)
        w = is_number(wb.get(), wheat)
        s = is_number(sb.get(), sugar)
        o = is_number(ob.get(), oil)
        mark(uid, "Rice", r)
        mark(uid, "Wheat", w)
        mark(uid, "Sugar", s)
        mark(uid, "Oil", o)
        update_count(uname, r, w, s, o, each)
        name.delete(0, 'end')
        blank1.delete(0, 'end')
        blank2.delete(0, 'end')
        blank3.delete(0, 'end')
        blank4.delete(0, 'end')
        rb.delete(0, 'end')
        wb.delete(0, 'end')
        sb.delete(0, 'end')
        ob.delete(0, 'end')
        check()

main = Tk()
main.resizable(0, 0)
fnt = (None, 20)

Label(main, text="Agent Aadhar", font=fnt).grid(row=0)
name = Entry(main, font=fnt)
name.grid(row=0, column=1)

Label(main, text="Available items", font=fnt).grid(row=1)
Label(main, text="Rice", font=fnt).grid(row=2, column=0)
blank1 = Entry(main, font=fnt)
blank1.grid(row=3, column=0)
Label(main, text="Wheat", font=fnt).grid(row=2, column=1)
blank2 = Entry(main, font=fnt)
blank2.grid(row=3, column=1)
Label(main, text="Sugar", font=fnt).grid(row=2, column=2)
blank3 = Entry(main, font=fnt)
blank3.grid(row=3, column=2)
Label(main, text="Oil", font=fnt).grid(row=2, column=3)
blank4 = Entry(main, font=fnt)
blank4.grid(row=3, column=3)
check()
rb = Entry(main, font=fnt)
rb.grid(row=4, column=0)
wb = Entry(main, font=fnt)
wb.grid(row=4, column=1)
sb = Entry(main, font=fnt)
sb.grid(row=4, column=2)
ob = Entry(main, font=fnt)
ob.grid(row=4, column=3)

Button(main, text='Quit', bg='red', font=fnt, command=main.destroy).\
    grid(row=5, column=0, sticky=W, pady=4)
Button(main, text='Assign items',bg='green', font=fnt, command=assign).\
    grid(row=5, column=1, sticky=W, pady=4)

mainloop()
