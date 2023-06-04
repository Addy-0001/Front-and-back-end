#import modules
from tkinter import *
import sqlite3
from tkinter import messagebox

#creating a window
window=Tk()
window.geometry("1280x720")
window.title("Room Booking")
icon=PhotoImage(file='icon.png')
window.iconphoto(TRUE,icon)

#background image
photo=PhotoImage(file='background2.png')
background=Label(window, image=photo).place(x=0,y=0)

#icon for navigation buttons
icon1=PhotoImage(file='Icons/Room.png')
icon2=PhotoImage(file='Icons/Customer.png')
icon3=PhotoImage(file='Icons/Book.png')
icon4=PhotoImage(file='Icons/Bill.png')
icon5=PhotoImage(file='Icons/Logout.png')

#connecting page
def open_cdetails():
    window.destroy()
    import Customer_Details

def open_rstatus():
    window.destroy()
    import Room_Status

def open_bill():
    window.destroy()
    import bill

def open_accounts():
    window.destroy()
    import accounts

#navigation panel
Frame(window,height=720,width=350,bg='black').place(x=0,y=0)

#navigation buttons
Button(image=icon1,compound=LEFT,text=' Room Status',font=('Times',20,'bold'),bg='black',fg='white',command=open_rstatus).place(x=0,y=0,height=72,width=350)
Button(image=icon2,compound=LEFT,text=' Customer Details',font=('Times',20,'bold'),bg='black',fg='white',command=open_cdetails).place(x=0,y=144,height=72,width=350)
Button(image=icon3,compound=LEFT,text= ' Room Booking',font=('Times',20,'bold'),fg='white',bg='#808080',activebackground='#808080',activeforeground='white').place(x=0,y=72,height=72,width=350)
Button(image=icon4,compound=LEFT,text=' Bill and Payment',font=('Times',20,'bold'),bg='black',fg='white',command=open_bill).place(x=0,y=216,height=72,width=350)
Button(image=icon5,compound=LEFT,text=' Accounts',font=('Times',20,'bold'),bg='black',fg='white',command=open_accounts).place(x=0,y=288,height=72,width=350)

#Room booking label
a=Frame(window,height=48,width=930,bg='white').place(x=350,y=150)
Label(window,text='Room Booking',bg='white',font=('Segoe Print',18)).place(x=725,y=150)

try:
    #creating a customer table
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("""CREATE TABLE customers(
        fname text,
        lname text,
        gender text,
        dob int,
        mob text,
        email text,
        address text,
        nationality text,
        days int,
        Room_Number text
    )""" )
    conn.commit()
    conn.close()
except:
    pass

#reset function
def reset():
    fn.delete(0,END)
    ln.delete(0,END)
    gen.delete(0,END)
    dob.delete(0,END)
    mob.delete(0,END)
    eml.delete(0,END)
    add.delete(0,END)
    nat.delete(0,END)
    cod.delete(0,END)
    rno.delete(0,END)

#teble function
def table():
    #setting all rooms to available
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Room_Number from room")
    avrooms=c.fetchall()
    for i in avrooms:
        c.execute("""UPDATE room SET
        Room_Status=:st""",{'st': 'Available'})
        conn.commit()
    conn.close()

    #updating rooms to occupied according to users
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Room_Number from customers")
    rnum=c.fetchall()
    for i in rnum:
        c.execute("""UPDATE room SET
        Room_Status=:st
        WHERE Room_Number=:rn""",{
            'st': 'Occupied',
            'rn': i[0]
        })
        conn.commit()
    conn.close()

    #creating a table
    table=Frame(window,height=580,width=950,bg='white')
    table.place(x=603,y=198)

    #connection with database
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT * from room")
    lst=c.fetchall()

    #table heading
    lst.insert(0,('S.No.','Room Number','Room Type','Status','Price'))

    #table
    total_rows =len(lst)
    total_columns=len(lst[1])
    for i in range(total_rows):
        #table heading
        if i==0:
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
            #setting colomn width
            if j==0:
                wid=7
            else:
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
    conn.commit()
    conn.close()

#fetch data function
def fetch():
    a=cid.get()
    if a=="":
        messagebox.showerror("Fetch","Enter CustomerID")
    else:
        try:
            #database connection
            conn=sqlite3.connect('booking.db')
            c=conn.cursor()
            c.execute("SELECT * from customers where oid=:cid",{'cid':a})
            rec=c.fetchall()
            #inserting values into entry boxes
            fn.insert(0,rec[0][0])
            ln.insert(0,rec[0][1])
            gen.insert(0,rec[0][2])
            dob.insert(0,rec[0][3])
            mob.insert(0,rec[0][4])
            eml.insert(0,rec[0][5])
            add.insert(0,rec[0][6])
            nat.insert(0,rec[0][7])
            cod.insert(0,rec[0][8])
            rno.insert(0,rec[0][9])
            conn.commit()
            conn.close()
            #update button status to normal
            upd.config(state=NORMAL)
        except:
            messagebox.showerror("Fetch","Invalid CustomerID")

#submit function
def submit():
    #add values to database
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("INSERT INTO customers VALUES (:fn, :ln, :gen, :dob, :mob, :email, :address, :nationality, :cod, :number)",
        {
            'fn':fn.get(),
            'ln':ln.get(),
            'gen':gen.get(),
            'dob':dob.get(),
            'mob':mob.get(),
            'email':eml.get(),
            'address':add.get(),
            'nationality':nat.get(),
            'cod':cod.get(),
            'number':rno.get()
        })
    conn.commit()

    #get customer id for just booked customer
    c.execute("SELECT oid from customers where mob=:phn",{'phn':mob.get()})
    cid=c.fetchall()

    #display customer id
    messagebox.showinfo("Booking","Room Booked Successfully, CustomerID: {}".format(cid[0][0]))
    conn.commit()
    conn.close()

    #update table
    table()
    #reset entries
    reset()

    try:
        #create bill for new customer
        conn=sqlite3.connect('booking.db')
        c=conn.cursor()
        c.execute("""CREATE TABLE bill(
            cid int,
            particular text,
            rate int,
            qty int,
            price int
        )""")
        conn.commit()
        conn.close()
    except:
        pass

    #get room number and number of days from customers table
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Room_Number,days from customers where oid=:cid",{'cid':cid[0][0]})
    room=c.fetchall()
    conn.commit()
    conn.close()

    #get price and room type from room table
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Price,Room_Type from room where Room_Number=:cid",{'cid':room[0][0]})
    price=c.fetchall()
    conn.commit()
    conn.close()
    days=room[0][1]
    rtype=price[0][1]
    prc=price[0][0]
    
    #inserting values to bill for room
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("INSERT INTO bill VALUES (:cid, :particular, :rate, :qty, :prc)",
    {
        'cid':cid[0][0],
        'particular':rtype,
        'rate':prc,
        'qty':days,
        'prc':prc*days
    })
    conn.commit()
    conn.close()

#verification for customer update
def verifyforupdate():
    #getting all occupied rooms and adding to a list
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Room_Number from room WHERE Room_Status=:oc",{'oc':"Occupied"})
    list1=c.fetchall()
    y=[]
    for i in list1:
        y.append(i[0])
    conn.commit()
    conn.close()

    #getting values to verify
    a=fn.get()
    b=ln.get()
    c=gen.get()
    d=dob.get()
    e=mob.get()
    f=eml.get()
    g=add.get()
    h=nat.get()
    i=cod.get()
    j=rno.get()

    #verification
    if a=="" or b=="" or c=="" or d=="" or e=="" or f=="" or g=="" or h=="" or i=="" or j=="":
        messagebox.showerror("Booking","One or More Fields Empty!")
    elif len(d)!=4:
        messagebox.showerror("Booking","Invalid Date")
    elif len(e)!=10:
        messagebox.showerror("Booking","Invalid Phone Number")
    elif "@" and ".com" not in f:
        messagebox.showerror("Booking","Invalid Email")
    elif j!="T1" and j!="T2" and j!="T3" and j!="C1" and j!="C2" and j!="R1" and j!="R2" and j!="R3" and j!="R4":
        messagebox.showerror("Booking","Invalid Room Number")
    elif d[0].isalpha() or d[1].isalpha() or d[2].isalpha() or d[3].isalpha():
        messagebox.showerror("Booking","Invalid Date")
    elif e[0].isalpha() or e[1].isalpha() or e[2].isalpha() or e[3].isalpha() or e[4].isalpha() or e[5].isalpha() or e[6].isalpha() or e[7].isalpha() or e[8].isalpha() or e[9].isalpha():
        messagebox.showerror("Booking","Invalid Phone Number")
    elif i[0].isalpha() or i[len(i)-1].isalpha() or len(i)>2:
        messagebox.showerror("Booking","Invalid Number of Days")
    else:
        #occupied room verification 
        if j in y:
            conn=sqlite3.connect('booking.db')
            c=conn.cursor()
            c.execute("SELECT Room_Number from customers where mob=:phn",{'phn':e})
            rn=c.fetchall()
            conn.commit()
            conn.close()
            if j==rn[0][0]:
                update()
            else:
                messagebox.showerror("Booking","Room Full")
        else:
            update()

#update function           
def update():
    a=rno.get()
    days=cod.get()
    
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("""UPDATE customers SET
        fname=:a,
        lname=:b,
        gender=:d,
        dob=:e,
        mob=:f,
        email=:g,
        address=:h,
        nationality=:i,
        days=:k,
        Room_Number=:l
        WHERE oid=:cid""",{
            'a':fn.get(),
            'b':ln.get(),
            'd':gen.get(),
            'e':dob.get(),
            'f':mob.get(),
            'g':eml.get(),
            'h':add.get(),
            'i':nat.get(),
            'k':cod.get(),
            'l':rno.get(),
            'cid':cid.get()
        })
    conn.commit()
    conn.close()
    reset()
    table()

    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Price, Room_Type from room WHERE Room_Number=:number",{'number':a})
    price=c.fetchall()
    conn.commit()
    conn.close()
    rtype=price[0][1]
    prc=price[0][0]
    summ=int(days)*int(prc)
    print(summ)

    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("""UPDATE bill SET
    particular=:newroom,
    rate=:price,
    qty=:days,
    price=:money WHERE cid=:cid""",{'newroom':rtype,'price':prc,'days':days,'money':summ,'cid':cid.get()})
    conn.commit()
    conn.close()

    messagebox.showinfo("Update","Data Updated Successfully")

#verification for submitting
def verifyforsubmit():
    conn=sqlite3.connect('booking.db')
    c=conn.cursor()
    c.execute("SELECT Room_Number from room WHERE Room_Status=:oc",{'oc':"Occupied"})
    list1=c.fetchall()
    y=[]
    for i in list1:
        y.append(i[0])
    conn.commit()
    conn.close()
    
    a=fn.get()
    b=ln.get()
    c=gen.get()
    d=dob.get()
    e=mob.get()
    f=eml.get()
    g=add.get()
    h=nat.get()
    i=cod.get()
    j=rno.get()
    if a=="" or b=="" or c=="" or d=="" or e=="" or f=="" or g=="" or h=="" or i=="" or j=="":
        messagebox.showerror("Booking","One or More Fields Empty!")
    elif len(d)!=4:
        messagebox.showerror("Booking","Invalid Date")
    elif len(e)!=10:
        messagebox.showerror("Booking","Invalid Phone Number")
    elif "@" and ".com" not in f:
        messagebox.showerror("Booking","Invalid Email")
    elif j!="T1" and j!="T2" and j!="T3" and j!="C1" and j!="C2" and j!="R1" and j!="R2" and j!="R3" and j!="R4":
        messagebox.showerror("Booking","Invalid Room Number")
    elif j in y:
        messagebox.showerror("Booking","Room Full")
    elif d[0].isalpha() or d[1].isalpha() or d[2].isalpha() or d[3].isalpha():
        messagebox.showerror("Booking","Invalid Date")
    elif i[0].isalpha() or i[len(i)-1].isalpha() or len(i)>2:
        messagebox.showerror("Booking","Invalid Number of Days")
    elif e[0].isalpha() or e[1].isalpha() or e[2].isalpha() or e[3].isalpha() or e[4].isalpha() or e[5].isalpha() or e[6].isalpha() or e[7].isalpha() or e[8].isalpha() or e[9].isalpha():
        messagebox.showerror("Booking","Invalid Phone Number")
    else:
        submit()

#Labels for data entry
Frame(window,bg='white',height=31,width=870).place(x=350,y=228)

Frame(window,bg='white',width=253,height=270).place(x=350,y=198)
Label(window,text='\u00BB       Book a Room',bg='white',font=('Agency FB',16,'bold')).place(x=350,y=188)
Label(window,text="Customer ID:",bg='white',font=('Agency FB',12)).place(x=355,y=230)
Label(window,text="First Name:",bg='white',font=('Agency FB',12)).place(x=355,y=255)
Label(window,text="Last Name:",bg='white',font=('Agency FB',12)).place(x=355,y=280)
Label(window,text="Gender:",bg='white',font=('Agency FB',12)).place(x=355,y=305)
Label(window,text="Year of Birth:",bg='white',font=('Agency FB',12)).place(x=355,y=330)
Label(window,text="Mobile:",bg='white',font=('Agency FB',12)).place(x=355,y=355)
Label(window,text="Email:",bg='white',font=('Agency FB',12)).place(x=355,y=380)
Label(window,text="Address:",bg='white',font=('Agency FB',12)).place(x=355,y=405)
Label(window,text="Nationality:",bg='white',font=('Agency FB',12)).place(x=355,y=430)

#Entry boxes
cid=Entry(window,relief=SOLID)
fn=Entry(window,relief=SOLID)
ln=Entry(window,relief=SOLID)
gen=Entry(window,relief=SOLID)
dob=Entry(window,relief=SOLID)
mob=Entry(window,relief=SOLID)
eml=Entry(window,relief=SOLID)
add=Entry(window,relief=SOLID)
nat=Entry(window,relief=SOLID)

cid.place(x=430,y=227,height=25,width=155)
fn.place(x=430,y=252,height=25,width=155)
ln.place(x=430,y=277,height=25,width=155)
gen.place(x=430,y=302,height=25,width=155)
dob.place(x=430,y=327,height=25,width=155)
mob.place(x=430,y=352,height=25,width=155)
eml.place(x=430,y=377,height=25,width=155)
add.place(x=430,y=402,height=25,width=155)
nat.place(x=430,y=427,height=25,width=155)

#entries for booking room
Frame(window,bg='white',width=253,height=130).place(x=350,y=468)
Label(window,text="No. of Nights:",bg='white',font=('Agency FB',12)).place(x=355,y=483)
Label(window,text="Room No.:",bg='white',font=('Agency FB',12)).place(x=355,y=508)

cod=Entry(window,relief=SOLID)
rno=Entry(window,relief=SOLID)

cod.place(x=430,y=485,height=25,width=155)
rno.place(x=430,y=510,height=25,width=155)

#buttons
Button(window,text="FETCH DATA",font=('Arial',8,'bold'),fg='white',bg="black",width=9,height=1,cursor='hand2',command=fetch).place(x=512, y=227)
Button(window,text="SAVE",font=('Arial',8,'bold'),fg='white',bg="black",width=6,height=1,cursor='hand2',command=verifyforsubmit).place(x=375, y=555)
upd=Button(window,text="UPDATE",font=('Arial',8,'bold'),fg='white',bg="black",width=6,height=1,cursor='hand2',state=DISABLED,command=verifyforupdate)
upd.place(x=445, y=555)
Button(window,text="RESET",font=('Arial',8,'bold'),fg='white',bg="black",width=6,height=1,cursor='hand2',command=reset).place(x=515, y=555)

table()

window.mainloop()