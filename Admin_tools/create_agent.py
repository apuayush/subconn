from pymongo import MongoClient
from config import var
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

client = MongoClient()
client = MongoClient(var.link, 27017)
db = client['subconn']
collection = db['agent_details']

def agent():
    uid = int(blank1.get())
    aid = str(blank2.get())
    pas = str(blank3.get())
    post = {"uid": uid, "uname": aid, "password": pas, "item_count": {"Rice": 0, "Wheat": 0, "Sugar": 0, "Oil": 0}}
    db.agent_details.insert(post)
    blank1.delete(0, 'end')
    blank2.delete(0, 'end')
    blank3.delete(0, 'end')


main = Tk()
main.resizable(0, 0)
fnt = (None, 20)

Label(main, text="Aadhaar number", font=fnt).grid(row=0)
Label(main, text="Agent id", font=fnt).grid(row=1)
Label(main, text="Password", font=fnt).grid(row=2)

blank1 = Entry(main, font=fnt)
blank1.grid(row=0, column=1)
blank2 = Entry(main, font=fnt)
blank2.grid(row=1, column=1)
blank3 = Entry(main, font=fnt)
blank3.grid(row=2, column=1)

Button(main, text='Quit', bg='red', font=fnt, command=main.destroy).\
    grid(row=3, column=0, sticky=W, pady=4)
Button(main, text='Create',bg='green', font=fnt, command=agent).\
    grid(row=3, column=1, sticky=W, pady=4)

mainloop()
