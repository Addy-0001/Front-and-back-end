#import necessary modules
from tkinter import *
from tkinter import messagebox
import random
import sqlite3

#creating a window
window=Tk()
window.geometry("1280x720")
window.title("Milestone Village Resort (Login)") #window title
photo = PhotoImage(file = 'icon.png')
window.iconphoto(True, photo) #window icon
#True makes it so that the icon is not specific to this page but also to all future created toplevels

#background image
photo2=PhotoImage(file='background.png')
background = Label(window, image = photo2).place(x=0, y=0) #since tkinter doesn't support background image, we place it as a label

#login function
def login():
    #signup page link
    def opensignup():
        window.destroy()
        import signup
    
    def openstatus():
        window.destroy()
        import Room_Status

#login frame
    Frame(window, height=440, width=350, bg='white').place(x=775, y=100) #frame for login box
    Frame(window, height=80, width=330, bg='#338bd7').place(x=785, y=110) #login frame title box
    Label(window, text='LOG IN', bg="#338bd7", fg='white', font=('Arial',20,'bold')).place(x=900, y=135)

    #authorization check
    def check():
        a=mail_ent.get()
        b=ps_ent.get()
        try:
            conn=sqlite3.connect('admins.db')
            c=conn.cursor()

            c.execute("SELECT * from users")
            records=c.fetchall()
            i=len(records)-1
            while i>=0:
                if records[i][2]!=a or records[i][4]!=b:
                    i=i-1
                    if i==-1:
                        messagebox.showerror("Login","Invalid Credentials")
                        break
                else:
                    #change user status to active after login and set other users as inactive
                    c.execute("""UPDATE users SET
                    status=:inactive
                    WHERE status=:active""",
                    {'inactive':False,
                    'active':True})
                    conn.commit()
                    
                    c.execute("""UPDATE users SET
                    status= :val
                    WHERE mail = :a""",
                    {
                        'val':True,
                        'a':a
                    })
                    conn.commit()
                    messagebox.showinfo("Login","Logged in Successfully")
                    openstatus()
                    break           
            conn.commit()
            conn.close()
        except:
            messagebox.showerror("Login","Sign Up First")

    #Tkinter does not support placeholders for entry so following two functions removes the default inserted text once the focus is on the entry box
    def remove(event):
        a=mail_ent.get()
        if a=='Enter Your Email':
            mail_ent.delete(0, END) #removes text in entry box from 0 index to end

    def remove2(event):
        b=ps_ent.get()  
        if b=='Enter Your Password': 
            ps_ent.delete(0, END)
        
    #email and password input
    mail_ent=Entry(window)
    mail_ent.insert(0, 'Enter Your Email') #default text inserted in entry box, 0 is positional argument
    mail_ent.place(x=805, y=220,width=290, height=30)
    mail_ent.bind('<FocusIn>', remove) #bind function is used to know the mouse movement (if it is clicked or hovering and so on)

    ps_ent=Entry(window)
    ps_ent.insert(0, 'Enter Your Password')
    ps_ent.place(x=805, y=270,width=210, height=30)
    ps_ent.bind('<FocusIn>', remove2)
    showw=IntVar(value=1)

    def show():
        if (showw.get()==1): #checkbutton passes value 1 for true and 0 for false
            ps_ent.config(show='') #config is used to access widget's attributes after its initialization
        else:
            ps_ent.config(show='*')

    #show password checkbutton
    Checkbutton(text='Show', offvalue=0, variable=showw, bg='white', command=show).place(x=1030, y=270)

    #login button
    Button(window,text="LOGIN",font=('Arial',10,'bold'),fg='white',bg="#338bd7",width=16,height=2,cursor='hand2',command=login).place(x=878, y=350)

    #forgot password and signup links
    Button(window,text="Forgot Password?", fg='blue', bg='white', cursor='hand2',command=reset).place(x=990, y=305)
    Label(window, text="New Employee?", bg='white').place(x=901, y=480)
    Button(window, text="SIGN UP NOW", fg='blue', bg='white', cursor='hand2',command=opensignup).place(x=904, y=503)

    #verification check
    def verify():
        a=mail_ent.get()
        b=ps_ent.get()
        if (a=="" or a=="Enter Your Email") or (b=="" or b=="Enter Your Password"):
            messagebox.showerror("Login","One or More Fields Empty.")
        elif "@" and ".com" not in a:
            messagebox.showerror("Password Reset","Invalid Email")
        elif len(b)<6:
            messagebox.showerror("Password Reset","Password must be more than 6 characters")
        else:
            check()

    #login button
    # Button(window, text="LOG IN", font=('Arial',10,'bold'), fg='white', bg="#338bd7", width=35, height=2, cursor='hand2',command=verify).place(x=805, y=350)

#forgot password functionality
def reset():

    #creating a toplevel
    top=Toplevel()
    top.geometry('380x350')
    top.title('Forgot Password')

    Frame(top,bg='#b4cef3',height=400,width=400).place(x=0,y=0)
    Label(top, text='RESET PASSWORD', bg="#b4cef3", fg='white', font=('Arial',20,'bold')).place(x=50, y=20)

    #remove functionalities for placeholders
    def remove(event):
        a=mail_ent.get()
        if a=='Enter Your Email':
            mail_ent.delete(0, END)

    def remove2(event):
        b=new_ps_ent.get()
        if b=='New Password':
            new_ps_ent.delete(0, END)

    def remove3(event):
        c=new_psc_ent.get()
        if c=='Confirm New Password':
            new_psc_ent.delete(0, END)

    #show password functionalities for passwords
    def show():
        if (showw.get()==1):
            new_ps_ent.config(show='')
        else:
            new_ps_ent.config(show='*')

    def show2():
        if (showww.get()==1):
            new_psc_ent.config(show='')
        else:
            new_psc_ent.config(show='*')
    
    #USER INPUTS
    mail_ent=Entry(top)
    mail_ent.insert(0, 'Enter Your Email')
    mail_ent.place(x=40, y=75,width=290, height=30)
    mail_ent.bind('<FocusIn>', remove)

    #security questions
    ans1=StringVar()
    a="Q1: What is your favourite food?"
    b="Q2: What is the name of your first pet?"
    c="Q3: What is the name of your childhood best friend?"
    lst=[a,b,c]
    ques=random.choice(lst)
    num=int(ques[1])-1
    Label(top,text=ques,bg='#b4cef3').place(x=40,y=118)
    Entry(top,textvariable=ans1).place(x=40,y=140,width=290,height=30)

    #new password
    new_ps_ent=Entry(top)
    new_ps_ent.insert(0, 'New Password') #default text inserted in entry box, 0 is positional argument
    new_ps_ent.place(x=40, y=190,width=210, height=30)
    new_ps_ent.bind('<FocusIn>', remove2) #bind function is used to know the mouse movement (if it is clicked or hovering and so on)
    showw=IntVar(value=1)
    Checkbutton(top,text='Show',offvalue=0,variable=showw,bg='#b4cef3',command=show).place(x=260,y=193)

    new_psc_ent=Entry(top)
    new_psc_ent.insert(0, 'Confirm New Password') #default text inserted in entry box, 0 is positional argument
    new_psc_ent.place(x=40, y=230,width=210, height=30)
    new_psc_ent.bind('<FocusIn>', remove3) #bind function is used to know the mouse movement (if it is clicked or hovering and so on)
    showww=IntVar(value=1)
    Checkbutton(top,text='Show',offvalue=0,variable=showww,bg='#b4cef3',command=show2).place(x=260,y=233)

    Button(top,text="CONFIRM",font=('Arial',10,'bold'),fg='white',bg="#338bd7",width=16,height=2,cursor='hand2',command=lambda:verify()).place(x=120, y=280)

    #update new password
    def update():
        a=mail_ent.get()
        b=ans1.get()
        
        #database connection for password update
        conn=sqlite3.connect('admins.db')
        c=conn.cursor()
        c.execute("SELECT * from users")
        records=c.fetchall()
        i=len(records)-1
        while i>=0:
            if records[i][2]!=a or records[i][(6+num)]!=b:
                i=i-1
                if i==-1:
                    messagebox.showerror("Password Reset","Invalid Credentials")
                    break
            else:
                ps_upd=new_ps_ent.get()
                psc_upd=new_psc_ent.get()
                c.execute("""UPDATE users SET
                ps= :new_ps,
                psc= :new_psc
                WHERE mail = :a""",
                {
                    'new_ps':ps_upd,
                    'new_psc':psc_upd,
                    'a':a
                })
                messagebox.showinfo("Password Reset","Password Changed Successfully")
                #destroy toplevel after successful password update
                top.destroy()
                break             
        conn.commit()
        conn.close()

    #password verification for forgot password functionality
    def verify():
        a=mail_ent.get()
        b=ans1.get()
        c=new_ps_ent.get()
        d=new_psc_ent.get()

        if a=="" or a=="Enter Your Email" or b=="" or c=="" or c=="New Password" or d=="" or d=="Confirm New Password":
            messagebox.showerror("Password Reset","One or More Fields Empty")
        else:
            if "@" and ".com" not in a:
                messagebox.showerror("Password Reset","Invalid Email")
            elif len(c)<6 or len(d)<6:
                messagebox.showerror("Password Reset","Password must be more than 6 characters")
            elif c!=d:
                messagebox.showerror("Password Reset","Passwords Mismatch")
            else:
                update()

login()

window.mainloop()