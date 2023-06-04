#import modules
from tkinter import *
import sqlite3
from tkinter import messagebox

#create a window
window=Tk()
window.geometry("1280x720")
window.title("Accounts")
icon=PhotoImage(file='icon.png')
window.iconphoto(TRUE,icon)

#image for background
photo=PhotoImage(file='background2.png')
background=Label(window, image=photo).place(x=0,y=0)

#icons for button
icon1=PhotoImage(file='Icons/Room.png')
icon2=PhotoImage(file='Icons/Customer.png')
icon3=PhotoImage(file='Icons/Book.png')
icon4=PhotoImage(file='Icons/Bill.png')
icon5=PhotoImage(file='Icons/Logout.png')

#connecting page
def open_rstatus():
    window.destroy()
    import Room_Status

def open_rbooking():
    window.destroy()
    import rbooking

def open_cdetails():
    window.destroy()
    import Customer_Details

def open_bill():
    window.destroy()
    import bill

#navigation panel
Frame(window,height=720,width=350,bg='black').place(x=0,y=0)

#navigation buttons
Button(image=icon1,compound=LEFT,text=' Room Status',font=('Times',20,'bold'),bg='black',fg='white',command=open_rstatus).place(x=0,y=0,height=72,width=350)
Button(image=icon2,compound=LEFT,text=' Customer Details',font=('Times',20,'bold'),bg='black',fg='white',command=open_cdetails).place(x=0,y=144,height=72,width=350)
Button(image=icon3,compound=LEFT,text= ' Room Booking',font=('Times',20,'bold'),bg='black',fg='white',command=open_rbooking).place(x=0,y=72,height=72,width=350)
Button(image=icon4,compound=LEFT,text=' Bill and Payment',font=('Times',20,'bold'),bg='black',fg='white',command=open_bill).place(x=0,y=216,height=72,width=350)
Button(image=icon5,compound=LEFT,text=' Accounts',font=('Times',20,'bold'),fg='white',bg='#808080',activebackground='#808080',activeforeground='white').place(x=0,y=288,height=72,width=350)

#Frame for account details
Frame(window, height=400, width=378, bg='white').place(x=600, y=220)

#label for account details
Label(window,text="First Name:",font=('Arial',10,'bold'),bg='white').place(x=620,y=240)
Label(window,text="Last Name:",font=('Arial',10,'bold'),bg='white').place(x=790,y=240)
Label(window,text="Email:",font=('Arial',10,'bold'),bg='white').place(x=620,y=310)
Label(window,text="Phone:",font=('Arial',10,'bold'),bg='white').place(x=620,y=380)
Label(window,text="Password:",font=('Arial',10,'bold'),bg='white').place(x=620,y=450)
Label(window,text="Confirm Password:",font=('Arial',10,'bold'),bg='white').place(x=790,y=450)

#fetch user data
try:
    conn=sqlite3.connect('admins.db')
    c=conn.cursor()
    c.execute("SELECT * from users WHERE status=:act",{'act':True})
    records=c.fetchall()
    a=records[0][0]
    b=records[0][1]
    c=records[0][2]
    d=records[0][3]
    e=records[0][4]
    f=records[0][5]
    conn.commit()
    conn.close()
except:
    a="First Name"
    b="Last Name"
    c="Email"
    d="Phone"
    e="Password"
    f="Confirm Password"

#show password functions
def show():
    if (showw.get()==1):
        ps.config(show='')
    else:
        ps.config(show='*')

def show2():
    if (showww.get()==1):
        psc.config(show='')
    else:
        psc.config(show='*')

#Entries for Account
fname=Entry(window)
fname.insert(0,a)
fname.place(x=620,y=265,width=160,height=30)

lname=Entry(window)
lname.insert(0,b)
lname.place(x=790,y=265,width=160,height=30)

mail=Entry(window)
mail.insert(0,c)
mail.place(x=620,y=335,width=330,height=30)

phone=Entry(window)
phone.insert(0,d)
phone.place(x=620,y=405,width=330,height=30)

ps=Entry(window,show='*')
ps.insert(0,e)
ps.place(x=620,y=475,width=160,height=30)
showw=IntVar(value=0)
Checkbutton(text='Show',offvalue=0,variable=showw,bg='white',command=show).place(x=620,y=505)

psc=Entry(window,show='*')
psc.insert(0,f)
psc.place(x=790,y=475,width=160,height=30)
showww=IntVar(value=0)
Checkbutton(text='Show',offvalue=0,variable=showww,bg='white',command=show2).place(x=790,y=505)

#logout function
def logout():
    msb=messagebox.askquestion("Logout","Are you sure you want to logout?")
    if msb=='yes':
        #set user status to inactive
        conn=sqlite3.connect('admins.db')
        c=conn.cursor()
        c.execute("""UPDATE users SET
        status= :off
        WHERE status= :on""",
        {
            'off':False,
            'on':True
        })
        conn.commit()
        conn.close()

        try:
        #destroy window and import logout
            window.destroy()
            import login
        except:
            pass

#verification for update
def verify():
    a=fname.get()
    b=lname.get()
    c=mail.get()
    d=phone.get()
    e=ps.get()
    f=psc.get()
         
    if (a=="" or a=="First Name") or (b=="" or b=="Last Name") or (c=="" or c=="Enter Your Email") or (d=="" or d=="Enter Your Phone Number") or (e=="" or e=="Create Password") or (f=="" or f=="Confirm Password"):
        messagebox.showerror("Signup","One or More Fields Empty.")
    elif "@" and ".com" not in c:
        messagebox.showerror("Signup","Invalid Email")
    elif len(e)<6 or len(f)<6:
        messagebox.showerror("Signup","Password must be more than 6 characters")
    elif len(d)!=10:
        messagebox.showerror("Signup","Invalid Phone Number Length")
    elif e!=f:
        messagebox.showerror("Signup","Passwords Mismatch")
    else:
        try:
            int(d)
            update()
        except:
            messagebox.showerror("Signup","Invalid Phone Number")   

#update function
def update():
    #database update
    conn=sqlite3.connect('admins.db')
    c=conn.cursor()
    c.execute("""UPDATE users SET
    fname=:a,
    lname=:b,
    mail=:d,
    phone=:e,
    ps=:f,
    psc=:g
    WHERE status=:act""",
    {
        'a':fname.get(),
        'b':lname.get(),
        'd':mail.get(),
        'e':phone.get(),
        'f':ps.get(),
        'g':psc.get(),
        'act':True
    })
    conn.commit()
    conn.close()

    #messagebox after update
    messagebox.showinfo("Accounts","Updated fields successfully!")

#delete function
def delete():
    msb=messagebox.askquestion("Delete","Are you sure you want to delete record?")
    if msb=='yes':
        conn=sqlite3.connect('admins.db')
        c=conn.cursor()
        c.execute("DELETE from users WHERE status=:act",{'act':True})
        conn.commit()
        conn.close()

        #import function
        window.destroy()
        import login

#update, delete and logout function
Button(window,text="UPDATE",font=('Arial',10,'bold'),fg='white',bg="black",width=12,height=2,cursor='hand2',command=verify).place(x=610, y=565)
Button(window,text="DELETE",font=('Arial',10,'bold'),fg='white',bg="black",width=12,height=2,cursor='hand2',command=delete).place(x=735, y=565)
Button(window,text="LOGOUT",font=('Arial',10,'bold'),fg='white',bg="black",width=12,height=2,cursor='hand2',command=logout).place(x=860, y=565)

#Account label
a=Frame(window,height=48,width=930,bg='white').place(x=350,y=150)
Label(window,text='Account',bg='white',font=('Segoe Print',18)).place(x=735,y=150)

window.mainloop()