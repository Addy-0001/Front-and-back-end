#import required modules
import sqlite3
from tkinter import *
from tkinter import messagebox

#creating a window
window=Tk()
window.geometry("1280x720")
window.title("Bill")
icon=PhotoImage(file='icon.png')
window.iconphoto(TRUE,icon)

#background image
photo=PhotoImage(file='background2.png')
background=Label(window, image=photo).place(x=0,y=0)

#icons in buttons
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

def open_accounts():
    window.destroy()
    import accounts

#navigation panel
Frame(window,height=720,width=350,bg='black').place(x=0,y=0)

#navigation buttons
Button(image=icon1,compound=LEFT,text=' Room Status',font=('Times',20,'bold'),bg='black',fg='white',command=open_rstatus).place(x=0,y=0,height=72,width=350)
Button(image=icon2,compound=LEFT,text=' Customer Details',font=('Times',20,'bold'),bg='black',fg='white',command=open_cdetails).place(x=0,y=144,height=72,width=350)
Button(image=icon3,compound=LEFT,text= ' Room Booking',font=('Times',20,'bold'),bg='black',fg='white',command=open_rbooking).place(x=0,y=72,height=72,width=350)
Button(image=icon4,compound=LEFT,text=' Bill and Payment',font=('Times',20,'bold'),fg='white',bg='#808080',activebackground='#808080',activeforeground='white').place(x=0,y=216,height=72,width=350)
Button(image=icon5,compound=LEFT,text=' Accounts',font=('Times',20,'bold'),bg='black',fg='white',command=open_accounts).place(x=0,y=288,height=72,width=350)

#bill and payment banner
a=Frame(window,height=83,width=930,bg='white').place(x=350,y=150)
Label(window,text='Bill and Payment',bg='white',font=('Segoe Print',18)).place(x=717,y=150)

#bill function
def bill():
    #reset function inside bill
    def reset():
        par.delete(0,END)
        rat.delete(0,END)
        qty.delete(0,END)

    #submit function for database update and connection
    def submit():
        #add a record to bill
        def add():
            a=search.get()
            conn=sqlite3.connect('booking.db')
            c=conn.cursor()
            c.execute("INSERT INTO bill VALUES (:cid, :particular, :rate, :qty, :prc)",
                {
                    'cid':a,
                    'particular':part,
                    'rate':rate,
                    'qty':quant,
                    'prc':rate*quant
                })
            conn.commit()
            conn.close()
            #update bill on screen
            bill()
        
        #getting the values from entry boxes
        part=par.get()
        rate=int(rat.get())
        quant=int(qty.get())
        a=len(lst)-1
        #if there is no previous entry, directly add to database
        if a==1:
            add()
        #if previous entries are present
        else:
            while a>1:
                #if that item of that price is present in database, update quantity of existing entry
                if part==lst[a][0] and rate==lst[a][1]:
                    conn=sqlite3.connect('booking.db')
                    c=conn.cursor()
                    c.execute("SELECT qty from bill where particular=:par",{'par':part})
                    oldqty=c.fetchall() #old quantity
                    conn.commit()
                    newqty=oldqty[0][0]+int(quant) #new quantity
                    #update quantity and price
                    c.execute("""UPDATE bill SET
                    qty=:newqt,
                    price=:newprice
                    WHERE particular=:par""",
                    {
                        'newqt':newqty,
                        'newprice':newqty*rate,
                        'par':part
                        })
                    conn.commit()
                    conn.close()
                    bill()
                    break
                else:
                    #if the entry is not already present in database, we add a new entry
                    a=a-1
                    if a==1:
                        add()

    #verification of bill entry               
    def verify():
        b=rat.get()
        c=qty.get()

        #if fields are empty
        if a=="" or b=="" or c=="":
            messagebox.showerror("Bill","Enter Necessary Fields!")
        #if number is negative
        elif b[0]=="-" or c[0]=="-":
            messagebox.showerror("Bill","Invalid Rate/Quantity")
        else:
            # check if entered data is integer
            try:
                int(b)
                int(c)
                submit()
            except:
                messagebox.showerror("Bill","Invalid Rate/Quantity")

    #Authentication check for user
    def verification():
        top=Toplevel()
        top.geometry('380x250')
        top.title('Confirm Your Authentication')

        #frame and label for toplevel
        Frame(top,bg='#b4cef3',height=400,width=400).place(x=0,y=0)
        Label(top, text='CONFIRM TRANSACTION', bg="#b4cef3", fg='white', font=('Arial',20,'bold')).place(x=22, y=20)

        #remove customer data after bill payment
        def removedata():
            msb=messagebox.askquestion("Bill","Are you sure?")
            if msb=='yes':
                conn=sqlite3.connect('booking.db')
                c=conn.cursor()
                c.execute("SELECT Room_Number from customers where oid=:cid",{'cid':search.get()})
                room=c.fetchall()
                c.execute("""UPDATE room SET Room_Status=:st where Room_Number=:num""",{'st':"Available",'num':room[0][0]})
                conn.commit()
                c.execute("DELETE from bill WHERE cid=:cus",{'cus':a})
                conn.commit()
                c.execute("DELETE from customers WHERE oid=:cid",{'cid':a})
                conn.commit()
                conn.close()
                messagebox.showinfo("Bill","Completed Transaction")
                
                window.destroy()
                import Room_Status

        #show password functionality for password
        def show():
            if (showw.get()==1):
                passw.config(show='')
            else:
                passw.config(show='*')

        #checking user password
        def confirm():
            try:
                conn=sqlite3.connect('admins.db')
                c=conn.cursor()
                c.execute("SELECT ps from users WHERE status=:act",{'act':True})
                ps=c.fetchall()
                conn.commit()
                conn.close()
                if ps[0][0]==passw.get():
                    removedata()
            except:
                messagebox.showerror("Bill","Unable to Process")

        #Entry for password
        Label(top,bg='#b4cef3',text='Password:',font=('Arial',11,'bold')).place(x=50,y=75)
        passw=Entry(top,relief=SOLID)
        passw.place(x=145,y=73,height=27,width=170)

        #checkbutton for password
        showw=IntVar(value=1)
        Checkbutton(top,text='Show',offvalue=0,variable=showw,bg='#b4cef3',command=show).place(x=145,y=108)

        #Button for confirm or cancel
        Button(top,text="CONFIRM",font=('Arial',10,'bold'),fg='white',bg="black",width=8,height=1,cursor='hand2',command=lambda:confirm()).place(x=100, y=160)
        Button(top,text="CANCEL",font=('Arial',10,'bold'),fg='white',bg="black",width=8,height=1,cursor='hand2',command=lambda:top.destroy()).place(x=195, y=160)  

    #Getting customer id
    a=search.get()
    
    #Fetching data for bill
    try:
        conn=sqlite3.connect('booking.db')
        c=conn.cursor()
        c.execute("SELECT particular, rate, qty, price from bill WHERE cid=:search",{'search':a})
        lst=c.fetchall()
        conn.commit()
        conn.close()

    #if data doesn't exist, use empty list    
    except:
        lst=[]
    
    #if list is empty, show error to the user
    if lst==[]:
        search.delete(0,END)
        messagebox.showerror("Bill","Invalid Customer ID")
    else:
        #add and display bill

        #Labels for entry
        Frame(window,bg='white',width=320,height=220).place(x=350,y=233)
        Label(window,bg='white',text='Particular:',font=('Arial',11,'bold')).place(x=370,y=270)
        Label(window,bg='white',text='Rate:',font=('Arial',11,'bold')).place(x=370,y=310)
        Label(window,bg='white',text='Quantity:',font=('Arial',11,'bold')).place(x=370,y=350)

        #Entry for bill items
        par=Entry(window,relief=SOLID)
        par.place(x=470,y=268,height=27,width=170)
        rat=Entry(window,relief=SOLID)
        rat.place(x=470,y=308,height=27,width=170)
        qty=Entry(window,relief=SOLID)
        qty.place(x=470,y=348,height=27,width=170)

        #Buttons
        Button(window,text="SAVE",font=('Arial',12,'bold'),fg='white',bg="black",width=6,height=1,cursor='hand2',command=verify).place(x=430, y=400)
        Button(window,text="RESET",font=('Arial',12,'bold'),fg='white',bg="black",width=6,height=1,cursor='hand2',command=reset).place(x=530, y=400)
        
        Frame(window,height=270,width=350,bg='white').place(x=800,y=350)
        #Heading of table
        lst.insert(0, ("Particular","Rate","Qty","Price"))

        def table():
        #Frame for table
            table=Frame(window,height=580,width=950,bg='white')
            table.place(x=803,y=350)

            #Creating a table
            total_rows =len(lst)
            total_columns=len(lst[0])
            for i in range(total_rows):
                #font for table heading
                if i==0:
                    fontt=('Arial',10,'bold')
                    ht=3
                #font for items in table
                else:
                    fontt=('Arial',10)
                    ht=1

                #setting width for individual column
                for j in range(total_columns):
                    if j==0:
                        jus=LEFT
                        wid=15
                    elif j==1:
                        jus=CENTER
                        wid=8
                    elif j==2:
                        jus=CENTER
                        wid=6
                    elif j==3:
                        jus=CENTER
                        wid=10
                    
                    #table
                    e=Label(
                        table,
                        width=wid,
                        font=fontt,
                        justify=jus,
                        bg='white',
                        height=ht
                    )
                    e.grid(row=i,column=j)
                    #table entries
                    e.config(text=(lst[i][j]))
            
            #calculating total price till now
            price=[]
            for i in range(1,len(lst)):
                price.append(lst[i][3])
            
            #display total
            Label(window,text="Total:",font=('Arial',10,'bold'),bg='white').place(x=1010,y=550)
            Label(window, text=(sum(price)),bg='white',font=('Arial',10)).place(x=1080,y=550)

        table()
        Button(window, text="Paid",font=('Arial',8,'bold'),fg='white',bg="black",width=8,height=1,cursor='hand2',command=verification).place(x=1060,y=575)

#Label for entering customer id
Label(window,text='\u00BB   Enter Customer ID:',bg='white',font=('Agency FB',16,'bold')).place(x=350,y=198)

#Bill Frame
Frame(window,height=370,width=350,bg='white').place(x=800,y=250)
#image for bill
photo2=PhotoImage(file='logo.png')
logo=Label(window, image=photo2).place(x=800,y=250)
#Billing resort deatails
Label(window,text="Milestone Village Resort",font=('Times',15,'bold'),bg='white').place(x=910,y=270)
Label(window,text="Prithivi Highway, Benighat, Dhading",font=('Times',10,),bg='white').place(x=916,y=300)
Label(window,text="Phone: 9841667426, 9803321885",font=('Times',8),bg='white').place(x=928,y=320)
#Entry and button to get bill of individual customer
search=Entry(window,relief=SOLID)
search.place(x=520,y=200,height=28,width=175)
Button(window, text="Get Bill",font=('Arial',8,'bold'),fg='white',bg="black",width=8,height=1,cursor='hand2',command=bill).place(x=700,y=201)

window.mainloop()