from Tkinter import *
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['subconn']

rice = db.generated_items.find({"name": "Rice", "assigned_to": "Unassigned"}).count()
wheat = db.generated_items.find({"name": "Wheat", "assigned_to": "Unassigned"}).count()
sugar = db.generated_items.find({"name": "Sugar", "assigned_to": "Unassigned"}).count()
oil = db.generated_items.find({"name": "Oil", "assigned_to": "Unassigned"}).count()

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
    uid = blank1.get()
    each = db.agent_details.find({"userid": uid})[0]
    if db.agent_details.find({"userid": uid}).count() == 1:
        r = is_number(rb.get(), rice)
        w = is_number(wb.get(), wheat)
        s = is_number(sb.get(), sugar)
        o = is_number(ob.get(), oil)
        db.agent_details.update({"userid": uid}, {'$set': {"Rice": each["Rice"]+r, "Wheat": each["Wheat"]+w, "Sugar": each["Sugar"]+s, "Oil": each["Oil"]+o}})
        blank1.delete(0, 'end')
        rb.delete(0, 'end')
        wb.delete(0, 'end')
        sb.delete(0, 'end')
        ob.delete(0, 'end')

main = Tk()
main.resizable(0, 0)
fnt = (None, 20)

Label(main, text="Agent id", font=fnt).grid(row=0)
blank1 = Entry(main, font=fnt)
blank1.grid(row=0, column=1)

Label(main, text="Available items", font=fnt).grid(row=1)
Label(main, text="Rice", font=fnt).grid(row=2, column=0)
Label(main, text=str(rice), font=fnt).grid(row=3, column=0)
Label(main, text="Wheat", font=fnt).grid(row=2, column=1)
Label(main, text=str(wheat), font=fnt).grid(row=3, column=1)
Label(main, text="Sugar", font=fnt).grid(row=2, column=2)
Label(main, text=str(sugar), font=fnt).grid(row=3, column=2)
Label(main, text="Oil", font=fnt).grid(row=2, column=3)
Label(main, text=str(oil), font=fnt).grid(row=3, column=3)

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
