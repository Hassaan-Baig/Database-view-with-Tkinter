import tkinter.messagebox
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *
from tkinter import Entry
import tkinter as tk
from tkcalendar import DateEntry

class Booking(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Appointment System')
        self.geometry('1500x600')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tree = self.create_tree_widget()

    def Root(self):
        return self.tree

    def create_tree_widget(self):
        columns = ('Book_id', 'Booking_date', 'App_date', 'Cust_id', 'Est_Price', 'Job_id')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('Book_id', text='Book_id')
        tree.heading('Booking_date', text='Booking_date')
        tree.heading('App_date', text='App_date')
        tree.heading('Cust_id', text='Cust_id')
        tree.heading('Est_Price', text='Est_Price')
        tree.heading('Job_id', text='Job_id')

        tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # generate sample data

        conn = None
        conn = connect("Booking.db")
        curs = conn.cursor()
        db = """create table IF NOT EXISTS  Booking(Book_id INT PRIMARY KEY, Booking_date TEXT, App_date TEXT, Cust_id INT,
        Est_Price INT, Job_id INT); """

        curs.execute(db)
        conn.commit()

        # add data to the treeview
        curs.execute("SELECT * FROM Booking")
        rows = curs.fetchall()
        conn.close()

        for row in rows:
            tree.insert('', tk.END, values=row)

        return tree

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            # show a message
            tkinter.messagebox.showinfo(title='Information', message=','.join(record))

    def add(self, attrs):
        conn = connect("Booking.db")
        curs = conn.cursor()
        data_tuple = tuple(attrs)
        query1 = '''INSERT OR IGNORE INTO Booking(Booking_date, App_date, Cust_id, Est_Price, Job_id) VALUES(?,?,?,?,?);'''

        curs.execute(query1, data_tuple)
        conn.commit()

        # add data to the treeview
        curs.execute("SELECT * FROM Booking")
        rows = curs.fetchall()
        conn.close()

        self.tree.insert('', tk.END, values=rows[-1])
        conn.close()

    def update(self, attrs):
        conn = connect("Booking.db")
        curs = conn.cursor()
        update_tuple = tuple(attrs)
        query1 = '''update Booking set Booking_date = ?, App_date = ?, Cust_id = ?,
        Est_Price = ?, Job_id = ? where Book_id = ? '''

        curs.execute(query1, update_tuple)
        conn.commit()
        self.tree.place_forget()
        # add data to the treeview
        curs.execute("SELECT * FROM Booking")
        rows = curs.fetchall()
        conn.close()
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def delete(self, id):
        conn = connect("Booking.db")
        curs = conn.cursor()
        query1 = '''delete from Booking where Book_id = ?'''

        curs.execute(query1, (id,))
        conn.commit()
        self.tree.place_forget()
        # add data to the treeview
        curs.execute("SELECT * FROM Booking")
        rows = curs.fetchall()
        conn.close()
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)


def BSearch(entry):
    # self.tree.selection()
    name = entry.get()
    print(name)
    broot.selection()
    fetchdata = broot.get_children()
    for f in fetchdata:
        broot.delete(f)
    conn = None
    try:
        conn = connect("Booking.db")
        core = conn.cursor()
        db = "select * from Booking where Book_id = '%s' "
        name = entry.get()
        if (len(name) < 0) :
            showerror("fail", "invalid name")
        else:
            core.execute(db % (name))
            data = core.fetchall()
            for d in data:
                broot.insert("", tk.END, values=d)

    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()


def BAddDatabase( bookingDate, appDate, custidEntry, estpriceEntry,
                                                           jobidEntry, labels, Addbutton):
    # Adding into list
    attributes = list()
    attributes.append(bookingDate.get())
    attributes.append(appDate.get())
    attributes.append(custidEntry.get())
    attributes.append(estpriceEntry.get())
    attributes.append(jobidEntry.get())
    print(attributes)
    bookingapp.add(attributes)
    bookingDate.place_forget()
    appDate.place_forget()
    custidEntry.place_forget()
    estpriceEntry.place_forget()
    jobidEntry.place_forget()
    for label in labels:
        label.place_forget()
    Addbutton.place_forget()


def BAddPage():
    # Booking
    label12 = tk.Label(broot, text='choose Booking Date')
    label12.place(x=120, y=500)
    # nameEntry = Entry(broot, width=10)
    bookingDate = DateEntry(broot, selectmode='day', textvariable=bookingDatestring)
    bookingDate.place(x=250, y=500)

    # App
    label13 = tk.Label(broot, text='choose App Date')
    label13.place(x=350, y=500)
    # nameEntry = Entry(broot, width=10)
    appDate = DateEntry(broot, selectmode='day', textvariable=appDatestring)
    appDate.place(x=460, y=500)

    # cust id
    label14 = tk.Label(broot, text='cust id')
    label14.place(x=570, y=500)
    custidEntry = Entry(broot, width=12)
    custidEntry.place(x=620, y=500)

    # Est_Price
    label15 = tk.Label(broot, text='Est_Price')
    label15.place(x=700, y=500)
    # global emailEntry
    estpriceEntry = Entry(broot, width=12)
    estpriceEntry.place(x=770, y=500)
    #
    # jobid
    label16 = tk.Label(broot, text='job_id')
    label16.place(x=850, y=500)
    # global phoneEntry
    jobidEntry = Entry(broot, width=12)
    jobidEntry.place(x=900, y=500)

    labels = [ label12, label13, label14, label15,label16 ]
    Addbutton = tkinter.Button(broot, text="Add",
                               command=lambda: BAddDatabase(bookingDate, appDate, custidEntry, estpriceEntry,
                                                           jobidEntry, labels, Addbutton))
    Addbutton.place(x=1000, y=500)


def BUpdateDatabase(idEntry, bookingDate, appDate, custidEntry, estpriceEntry,
                                                           jobidEntry, labels, Addbutton):
    # Adding into list
    attributes = list()
    attributes.append(bookingDate.get())
    attributes.append(appDate.get())
    attributes.append(custidEntry.get())
    attributes.append(estpriceEntry.get())
    attributes.append(jobidEntry.get())
    attributes.append(idEntry.get())

    print(attributes)
    bookingapp.update(attributes)
    bookingDate.place_forget()
    appDate.place_forget()
    custidEntry.place_forget()
    estpriceEntry.place_forget()
    jobidEntry.place_forget()
    idEntry.place_forget()
    for label in labels:
        label.place_forget()
    Addbutton.place_forget()



def BUpdatePage():
    # ID
    label11 = tk.Label(broot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(broot, width=10)
    idEntry.place(x=40, y=500)

    # Booking
    label12 = tk.Label(broot, text='choose Booking Date')
    label12.place(x=120, y=500)
    # nameEntry = Entry(broot, width=10)
    bookingDate = DateEntry(broot, selectmode='day', textvariable=bookingDatestring)
    bookingDate.place(x=250, y=500)

    # App
    label13 = tk.Label(broot, text='choose App Date')
    label13.place(x=350, y=500)
    # nameEntry = Entry(broot, width=10)
    appDate = DateEntry(broot, selectmode='day', textvariable=appDatestring)
    appDate.place(x=460, y=500)

    # cust id
    label14 = tk.Label(broot, text='cust id')
    label14.place(x=570, y=500)
    custidEntry = Entry(broot, width=12)
    custidEntry.place(x=620, y=500)

    # Est_Price
    label15 = tk.Label(broot, text='Est_Price')
    label15.place(x=700, y=500)
    # global emailEntry
    estpriceEntry = Entry(broot, width=12)
    estpriceEntry.place(x=770, y=500)
    #
    # jobid
    label16 = tk.Label(broot, text='job_id')
    label16.place(x=850, y=500)
    # global phoneEntry
    jobidEntry = Entry(broot, width=12)
    jobidEntry.place(x=900, y=500)

    labels = [ label11, label12, label13, label14, label15,label16 ]
    Addbutton = tkinter.Button(broot, text="Add",
                               command=lambda: BUpdateDatabase(idEntry, bookingDate, appDate, custidEntry, estpriceEntry,
                                                           jobidEntry, labels, Addbutton))
    Addbutton.place(x=1000, y=500)



def BDeleteDatabase(idEntry, label11,deletebutton):
    print(idEntry.get())
    bookingapp.delete(idEntry.get())
    idEntry.place_forget()
    label11.place_forget()
    deletebutton.place_forget()


# Delete Page
def BDeletePage():
    # ID
    label11 = tk.Label(broot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(broot, width=10)
    idEntry.place(x=40, y=500)
    deletebutton = tkinter.Button(broot, text="Delete",
                                  command=lambda: BDeleteDatabase(idEntry, label11,
                                                                 deletebutton))
    deletebutton.place(x=100, y=500)


def MainBooking():
    global bookingapp
    bookingapp= Booking()

    global bookingDatestring
    bookingDatestring= tkinter.StringVar()  # declaring string variable
    global appDatestring
    appDatestring= tkinter.StringVar()  # declaring string variable

    bList1 = [ 1, '2/10/21', '2/12/22', 1, 2, 10 ]
    bList2 = [ 2, '3/9/21', '4/11/22', 2, 12, 100 ]

    updateList2 = [ '10/9/21', '4/11/22', 2, 12, 100, 2 ]

    global broot
    broot= bookingapp.Root()

    label1 = tkinter.Label(broot, text="Search", font=("straight", 11, "bold"))
    label1.place(x=10, y=526)

    entry = Entry(broot, width=20)
    entry.place(x=100, y=526)

    button = tkinter.Button(broot, text="Search", command=lambda : BSearch(entry))
    button.place(x=250, y=526)

    bt1 = tk.Button(broot, text='Add Form', command=BAddPage)
    bt1.place(x=310, y=526)

    bt2 = tk.Button(broot, text='update Form', command=BUpdatePage)
    bt2.place(x=390, y=526)

    bt3 = tk.Button(broot, text='Delete Form', command=BDeletePage)
    bt3.place(x=485, y=526)

    bookingapp.mainloop()


# Main()
# MainBooking()
