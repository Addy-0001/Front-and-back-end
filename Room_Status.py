#import modules
from tkinter import *
import sqlite3

#create a window
window=Tk()
window.geometry("1280x720")
window.title("Room Status")
icon=PhotoImage(file='icon.png')
window.iconphoto(TRUE,icon)

#background image
photo=PhotoImage(file='background2.png')
background=Label(window, image=photo).place(x=0,y=0)

#icons for buttons
icon1=PhotoImage(file='Icons/Room.png')
icon2=PhotoImage(file='Icons/Customer.png')
icon3=PhotoImage(file='Icons/Book.png')
icon4=PhotoImage(file='Icons/Bill.png')
icon5=PhotoImage(file='Icons/Logout.png')

#connecting page
def open_cdetails():
    window.destroy()
    import Customer_Details

def open_rbooking():
    window.destroy()
    import rbooking

def open_bill():
    window.destroy()
    import bill

def open_accounts():
    window.destroy()
    import accounts

#navigation panel
Frame(window,height=720,width=350,bg='black').place(x=0,y=0)

#navigation buttons
Button(image=icon1,compound=LEFT,text=' Room Status',font=('Times',20,'bold'),fg='white',bg='#808080',activebackground='#808080',activeforeground='white').place(x=0,y=0,height=72,width=350)
Button(image=icon2,compound=LEFT,text=' Customer Details',font=('Times',20,'bold'),bg='black',fg='white',command=open_cdetails).place(x=0,y=144,height=72,width=350)
Button(image=icon3,compound=LEFT,text= ' Room Booking',font=('Times',20,'bold'),bg='black',fg='white',command=open_rbooking).place(x=0,y=72,height=72,width=350)
Button(image=icon4,compound=LEFT,text=' Bill and Payment',font=('Times',20,'bold'),bg='black',fg='white',command=open_bill).place(x=0,y=216,height=72,width=350)
Button(image=icon5,compound=LEFT,text=' Accounts',font=('Times',20,'bold'),bg='black',fg='white',command=open_accounts).place(x=0,y=288,height=72,width=350)

#room status frame and label
a=Frame(window,height=48,width=930,bg='white').place(x=350,y=150)
Label(window,text='Room Status',bg='white',font=('Segoe Print',18)).place(x=725,y=150)

#Frame for table
table=Frame(window,height=580,width=950,bg='white')
table.place(x=351,y=200)

#fetching data from database
conn=sqlite3.connect('booking.db')
c=conn.cursor()
c.execute("SELECT * from room")
lst=c.fetchall()

#table headings
lst.insert(0,('S.No.','Room Number','Room Type','Status','Price'))
print(lst)

#creating a table
total_rows =len(lst)
total_columns=len(lst[1])

for i in range(total_rows):
    if i==0:
        #table heading
        fontt=('Arial',16,'bold')
        jus=CENTER
        bgc='#9cc2e5'
    else:
        #table data
        fontt=('Arial',16)
        jus=LEFT
        state=(lst[i][3])
        if state=="Occupied":
            bgc='#f79b9b'
        else:
            bgc='#a8d08d'

    for j in range(total_columns):
        #first column
        if j==0:
            wid=7
        else:
            #other columns
            wid=16
        e=Entry(
            table,
            width=wid,
            font=fontt,
            justify=jus,
            disabledforeground='black',
            disabledbackground=bgc
        )
        e.grid(row=i,column=j)
        e.insert(0,lst[i][j])
        e.config(state=DISABLED)

#Last column
price=Entry(window,font=('Arial',16,'bold'),justify=CENTER,disabledbackground='#9cc2e5',disabledforeground='black')
price.insert(0,"Price")
price.config(state=DISABLED)
price.place(x=1026,y=200)

room=Entry(window,font=('Arial',14),justify=CENTER,bg='white',disabledbackground='white',disabledforeground='black')
room.insert(0,"Rs.2000/- per night")
room.config(state=DISABLED)
room.place(x=1026,y=228,height=112,width=244)

cottage=Entry(window,font=('Arial',14),justify=CENTER,bg='white',disabledbackground='white',disabledforeground='black')
cottage.insert(0,"Rs.1750/- per night")
cottage.config(state=DISABLED)
cottage.place(x=1026,y=340,height=57,width=244)

tent=Entry(window,font=('Arial',14),justify=CENTER,bg='white',disabledbackground='white',disabledforeground='black')
tent.insert(0,"Rs.1500/- per night")
tent.config(state=DISABLED)
tent.place(x=1026,y=396,height=84,width=244)

window.mainloop()