#import modules
from tkinter import *
from tkinter import messagebox
import sqlite3

#create window
window=Tk()
window.geometry("1280x720") #window size
window.title("Milestone Village Resort (Sign Up)") #window title
photo = PhotoImage(file = 'icon.png')
window.iconphoto(False,photo) #window icon

#background image
photo2=PhotoImage(file='background.png')
bg = Label(window, image = photo2).place(x=0,y=0) #since tkinter doesn't support background image, we place it as a label

#creating a database table
try:
    conn=sqlite3.connect('admins.db')
    c=conn.cursor()
    c.execute("""CREATE TABLE users(
        fname text,
        lname text,
        mail text PRIMARY KEY,
        phone text,
        ps text,
        psc text,
        q1 text,
        q2 text,
        q3 text,
        status boolean
    )""" )
    conn.commit()
    conn.close()
except:
    pass

#signup function
def signup():
    def openlogin():
        window.destroy()
        import login

    #remove functions are used as placeholders so that when users click on the entry box, inserted text is deleted
    def remove(event):
        a=fname_ent.get()
        if a=="First Name":
            fname_ent.delete(0, END)

    def remove1(event):
        a=lname_ent.get()
        if a=="Last Name":
            lname_ent.delete(0, END)

    def remove2(event):
        a=mail_ent.get()
        if a=="Enter Your Email":
            mail_ent.delete(0, END)

    def remove3(event):
        a=phone_ent.get()
        if a=="Enter Your Phone Number":
            phone_ent.delete(0, END)

    def remove4(event):
        a=ps_ent.get()
        if a=="Create Password":
            ps_ent.delete(0, END)

    def remove5(event):
        a=psc_ent.get()
        if a=="Confirm Password":
            psc_ent.delete(0, END)

    #show password functions for passwords
    def show():
        if (showw.get()==1):
            ps_ent.config(show='')
        else:
            ps_ent.config(show='*')

    def show2():
        if (showww.get()==1):
            psc_ent.config(show='')
        else:
            psc_ent.config(show='*')

    #signup frame
    Frame(window, height=440,width=350,bg='white').place(x=775,y=100)
    Frame(window, height=80,width=330,bg='#338bd7').place(x=785,y=110)
    Label(window,text='SIGN UP',bg="#338bd7",fg='white',font=('Arial',20,'bold')).place(x=895,y=135)

    #email and password input
    fname_ent=Entry(window)
    fname_ent.insert(0, 'First Name')
    fname_ent.place(x=805, y=220, width=130,height=30)
    fname_ent.bind('<FocusIn>', remove) #bind function is used to montior the movement of mouse

    lname_ent=Entry(window)
    lname_ent.insert(0, 'Last Name')
    lname_ent.place(x=965, y=220, width=130,height=30)
    lname_ent.bind('<FocusIn>', remove1)

    mail_ent=Entry(window)
    mail_ent.insert(0, 'Enter Your Email')
    mail_ent.place(x=805, y=265, width=290, height=30)
    mail_ent.bind('<FocusIn>', remove2)

    phone_ent=Entry(window)
    phone_ent.insert(0, 'Enter Your Phone Number')
    phone_ent.place(x=805, y=310, width=290, height=30)
    phone_ent.bind('<FocusIn>', remove3)

    ps_ent=Entry(window)
    ps_ent.insert(0, 'Create Password')
    ps_ent.place(x=805, y=355, width=210, height=30)
    ps_ent.bind('<FocusIn>', remove4)
    showw=IntVar(value=1)
    Checkbutton(text='Show',offvalue=0,variable=showw,bg='white',command=show).place(x=1030,y=355) #show password checkbutton

    psc_ent=Entry(window)
    psc_ent.insert(0, 'Confirm Password')
    psc_ent.place(x=805, y=400, width=210, height=30)
    psc_ent.bind('<FocusIn>', remove5)
    showww=IntVar(value=1)
    Checkbutton(text='Show',offvalue=0,variable=showww,bg='white',command=show2).place(x=1030,y=400)

    #verification function to check the validation of entered data
    def verify():
        a=fname_ent.get()
        b=lname_ent.get()
        c=mail_ent.get()
        d=phone_ent.get()
        e=ps_ent.get()
        f=psc_ent.get()
            
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
                sques()
            except:
                messagebox.showerror("Signup","Invalid Phone Number")

    #next and back button
    Button(window,text="BACK (LOGIN)",font=('Arial',10,'bold'),fg='white',bg="#338bd7",width=16,height=2,cursor='hand2',command=openlogin).place(x=800, y=475)
    Button(window,text="NEXT",font=('Arial',10,'bold'),fg='white',bg="#338bd7",width=16,height=2,cursor='hand2',command=verify).place(x=962, y=475)

    #function for security question
    def sques():
        a=StringVar()
        b=StringVar()
        d=StringVar()

        Frame(height=330,width=350,bg='white').place(x=775,y=210)
        
        Label(text="Security Questions",font=('Arial',16,'bold'),bg='white').place(x=847,y=210)

        Label(text="Q1: What is your favourite food?",bg='white').place(x=805,y=255)
        Entry(window, textvariable=a).place(x=805, y=280, width=290, height=30)
        
        Label(text="Q2: What is the name of your first pet?",bg='white').place(x=805,y=330)
        Entry(window, textvariable=b).place(x=805, y=350, width=290, height=30)

        Label(text="Q3: What is the name of your childhood best friend?",bg='white').place(x=805,y=400)
        Entry(window,textvariable=d).place(x=805, y=420, width=290, height=30)

        #verification for security questions
        def verify2():
            aa=a.get()
            bb=b.get()
            cc=d.get()

            if aa=="" or bb=="" or cc=="":
                messagebox.showerror("Security Questions","One or more fields empty")
            else:
                submit()

        #database connection for signup
        def submit():
            conn=sqlite3.connect('admins.db')
            c=conn.cursor()
            c.execute("INSERT INTO users VALUES (:fname_ent, :lname_ent, :mail_ent, :phone_ent, :ps_ent, :psc_ent, :q1, :q2, :q3, :status)",
            {
                'fname_ent':fname_ent.get(),
                'lname_ent':lname_ent.get(),
                'mail_ent':mail_ent.get(),
                'phone_ent':phone_ent.get(),
                'ps_ent':ps_ent.get(),
                'psc_ent':psc_ent.get(),
                'q1':a.get(),
                'q2':b.get(),
                'q3':d.get(),
                'status':False
                })
            conn.commit()
            conn.close()

            messagebox.showinfo("Signup","User Registered Successfully")

            openlogin()

        #signup button
        Button(window,text="SIGN UP",font=('Arial',10,'bold'),fg='white',bg="#338bd7",width=35,height=2,cursor='hand2',command=verify2).place(x=805, y=475)

signup()

window.mainloop()