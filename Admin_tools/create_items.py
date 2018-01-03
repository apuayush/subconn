from datetime import *
from pymongo import MongoClient
import uuid
from config import var
#import pprint

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

client = MongoClient()
client = MongoClient(var.link, 27017)
db = client['subconn']
collection = db['items']
p_list = []

ch = ''


def sel():
    global ch
    ch = str(var.get())


def item_generator(item_name, item_quantity, item_exp):
    nw = datetime.now()
    da = timedelta(days=item_exp)
    ex = (nw + da).__str__()[:10]
    nw = nw.__str__()[:10]
    #print nw, ex
    for _ in range(item_quantity):
        post = {"name": item_name, "packaging_date": str(nw), "expiry_date":\
            str(ex), "code": item_name+"|"+str(uuid.uuid4())+"|"+str(ex), "transaction_id": "None", "assigned_to": "Factory"}
        p_list.append(post)


def is_number(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 0


def show_answer():
    val = ''
    if ch == '1':
        val = 'Rice'
        exp = 2*365
    elif ch == '2':
        val = 'Wheat'
        exp = 6*30
    elif ch == '3':
        val = 'Sugar'
        exp = 2*365
    else:
        val = 'Oil'
        exp = 365
    quan = is_number(blank1.get())
    item_generator(val, quan, exp)
    blank1.delete(0, 'end')
    if len(p_list)>0:
        #pprint.pprint(p_list)
        db.items.insert_many(p_list)
        del p_list[:]


main = Tk()
main.resizable(0, 0)
fnt = (None, 20)

Label(main, text="Choose Item", font=fnt).grid(row=0)
Label(main, text="Enter Quantity", font=fnt).grid(row=3)

var = IntVar()
R1 = Radiobutton(main, text="Rice", variable=var, value=1, font=fnt,\
    command=sel)
R2 = Radiobutton(main, text="Wheat", variable=var, value=2, font=fnt,\
    command=sel)
R3 = Radiobutton(main, text="Sugar", variable=var, value=3, font=fnt,\
    command=sel)
R4 = Radiobutton(main, text="Oil", variable=var, value=4, font=fnt,\
    command=sel)

blank1 = Entry(main, font=fnt)
blank1.grid(row=3, column=1)
R1.grid(row=1, column=0)
R2.grid(row=1, column=1)
R3.grid(row=2, column=0)
R4.grid(row=2, column=1)

Button(main, text='Quit', bg='red', font=fnt, command=main.destroy).\
    grid(row=4, column=0, sticky=W, pady=4)
Button(main, text='Add records',bg='green', font=fnt, command=show_answer).\
    grid(row=4, column=1, sticky=W, pady=4)

mainloop()
