import tkinter.messagebox
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *
from tkinter import Entry
import tkinter as tk


class App(tk.Tk):
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
        columns = ('Cust_id', 'Name', 'Surname', 'Email', 'P.no', 'Address', 'City', 'Postcode')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('Cust_id', text='Cust Id')
        tree.heading('Name', text='Name')
        tree.heading('Surname', text='Surname')
        tree.heading('Email', text='Email')
        tree.heading('P.no', text='Pno')
        tree.heading('Address', text='Address')
        tree.heading('City', text='City')
        tree.heading('Postcode', text='PostCode')

        tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # generate sample data

        conn = None
        conn = connect("cust.db")
        curs = conn.cursor()
        db = """create table IF NOT EXISTS  Customers(Cust_id INTEGER PRIMARY KEY NOT NULL, Name TEXT, Surname TEXT, Email TEXT,
        Pno INT, Address TEXT,City TEXT,Postcode TEXT); """

        curs.execute(db)
        conn.commit()

        # add data to the treeview
        curs.execute("SELECT * FROM Customers")
        rows = curs.fetchall()
        conn.close()

        for row in rows:
            tree.insert('', tk.END, values=row)

        return tree

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item[ 'values' ]
            # show a message
            tkinter.messagebox.showinfo(title='Information', message=','.join(record))

    def add(self, attrs):
        conn = connect("cust.db")
        curs = conn.cursor()
        data_tuple = tuple(attrs)
        query1 = '''INSERT OR IGNORE INTO Customers(Name, Surname,Email, Pno, Address, City, Postcode) VALUES(?,?,?,
        ?,?,?,?); '''

        curs.execute(query1, data_tuple)
        conn.commit()

        # add data to the treeview
        curs.execute("SELECT * FROM Customers")
        rows = curs.fetchall()
        conn.close()

        self.tree.insert('', tk.END, values=rows[-1])
        conn.close()

    def update(self, attrs):
        conn = connect("cust.db")
        curs = conn.cursor()
        update_tuple = tuple(attrs)
        query1 = '''update Customers set Name = ?, Surname = ?, Email = ?,Pno  = ?, Address  = ?,City  = ?,Postcode = 
        ? where Cust_id = ? '''

        curs.execute(query1, update_tuple)
        conn.commit()
        self.tree.place_forget()
        # add data to the treeview
        curs.execute("SELECT * FROM Customers")
        rows = curs.fetchall()
        conn.close()
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def delete(self, id):
        conn = connect("cust.db")
        curs = conn.cursor()
        query1 = '''delete from Customers where Cust_id = ?'''

        curs.execute(query1, (id,))
        conn.commit()
        self.tree.place_forget()
        # add data to the treeview
        curs.execute("SELECT * FROM Customers")
        rows = curs.fetchall()
        conn.close()
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

def CSearch(entry):
    # self.tree.selection()
    name = entry.get()
    print(name)
    croot.selection()
    fetchdata = croot.get_children()
    for f in fetchdata:
        croot.delete(f)
    conn = None
    try:
        conn = connect("cust.db")
        core = conn.cursor()
        db = "select * from Customers where Name = '%s' "
        name = entry.get()
        if (len(name) < 2) or (not name.isalpha()):
            showerror("fail", "invalid name")
        else:
            core.execute(db % (name))
            data = core.fetchall()
            for d in data:
                croot.insert("", tk.END, values=d)

    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close()


#     Adding into database

def CAddDatabase(nameEntry, surnameEntry, emailEntry, phoneEntry, addressEntry, cityEntry, pcodeEntry, labels,
                btn):
    # Adding into list
    attributes = list()
    attributes.append(nameEntry.get())
    attributes.append(surnameEntry.get())
    attributes.append(emailEntry.get())
    attributes.append(phoneEntry.get())
    attributes.append(addressEntry.get())
    attributes.append(cityEntry.get())
    attributes.append(pcodeEntry.get())
    print(attributes)
    Capp.add(attributes)
    pcodeEntry.place_forget()
    cityEntry.place_forget()
    addressEntry.place_forget()
    phoneEntry.place_forget()
    emailEntry.place_forget()
    surnameEntry.place_forget()
    nameEntry.place_forget()
    for label in labels:
        label.place_forget()
    btn.place_forget()


def CAddPage():

    # Name
    label12 = tk.Label(croot, text='Name')
    label12.place(x=120, y=500)
    # global nameEntry
    nameEntry = Entry(croot, width=10)
    nameEntry.place(x=170, y=500)

    # surname
    label13 = tk.Label(croot, text='Surname')
    label13.place(x=250, y=500)
    # global surnameEntry
    surnameEntry = Entry(croot, width=12)
    surnameEntry.place(x=310, y=500)

    # Email
    label14 = tk.Label(croot, text='Email')
    label14.place(x=400, y=500)
    # global emailEntry
    emailEntry = Entry(croot, width=12)
    emailEntry.place(x=450, y=500)

    # Phone
    label15 = tk.Label(croot, text='Phone')
    label15.place(x=550, y=500)
    # global phoneEntry
    phoneEntry = Entry(croot, width=12)
    phoneEntry.place(x=600, y=500)

    # Address
    label16 = tk.Label(croot, text='Address')
    label16.place(x=700, y=500)
    # global addressEntry
    addressEntry = Entry(croot, width=12)
    addressEntry.place(x=750, y=500)

    # City
    label17 = tk.Label(croot, text='City')
    label17.place(x=850, y=500)
    # global cityEntry
    cityEntry = Entry(croot, width=10)
    cityEntry.place(x=900, y=500)

    # PostCode
    label18 = tk.Label(croot, text='Pcode')
    label18.place(x=970, y=500)
    # global pcodeEntry
    pcodeEntry = Entry(croot, width=10)
    pcodeEntry.place(x=1020, y=500)
    labels = [label12, label13, label14, label15, label16, label17, label18 ]
    Addbutton = tkinter.Button(croot, text="Add",
                               command=lambda: CAddDatabase(nameEntry, surnameEntry, emailEntry, phoneEntry,
                                                           addressEntry, cityEntry, pcodeEntry, labels, Addbutton))
    Addbutton.place(x=1070, y=500)


# Update into database

def CUpdateDatabase(idEntry, nameEntry, surnameEntry, emailEntry, phoneEntry, addressEntry, cityEntry, pcodeEntry, labels, btn):
    # Adding into list
    attributes = list()
    attributes.append(nameEntry.get())
    attributes.append(surnameEntry.get())
    attributes.append(emailEntry.get())
    attributes.append(phoneEntry.get())
    attributes.append(addressEntry.get())
    attributes.append(cityEntry.get())
    attributes.append(pcodeEntry.get())
    attributes.append(idEntry.get())
    print(attributes)
    Capp.update(attributes)
    pcodeEntry.place_forget()
    cityEntry.place_forget()
    addressEntry.place_forget()
    phoneEntry.place_forget()
    emailEntry.place_forget()
    surnameEntry.place_forget()
    nameEntry.place_forget()
    idEntry.place_forget()
    for label in labels:
        label.place_forget()
    btn.place_forget()


def CUpdatePage():
    # ID
    label11 = tk.Label(croot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(croot, width=10)
    idEntry.place(x=40, y=500)

    # Name
    label12 = tk.Label(croot, text='Name')
    label12.place(x=120, y=500)
    # global nameEntry
    nameEntry = Entry(croot, width=10)
    nameEntry.place(x=170, y=500)

    # surname
    label13 = tk.Label(croot, text='Surname')
    label13.place(x=250, y=500)
    # global surnameEntry
    surnameEntry = Entry(croot, width=12)
    surnameEntry.place(x=310, y=500)

    # Email
    label14 = tk.Label(croot, text='Email')
    label14.place(x=400, y=500)
    # global emailEntry
    emailEntry = Entry(croot, width=12)
    emailEntry.place(x=450, y=500)

    # Phone
    label15 = tk.Label(croot, text='Phone')
    label15.place(x=550, y=500)
    # global phoneEntry
    phoneEntry = Entry(croot, width=12)
    phoneEntry.place(x=600, y=500)

    # Address
    label16 = tk.Label(croot, text='Address')
    label16.place(x=700, y=500)
    # global addressEntry
    addressEntry = Entry(croot, width=12)
    addressEntry.place(x=750, y=500)

    # City
    label17 = tk.Label(croot, text='City')
    label17.place(x=850, y=500)
    # global cityEntry
    cityEntry = Entry(croot, width=10)
    cityEntry.place(x=900, y=500)

    # PostCode
    label18 = tk.Label(croot, text='Pcode')
    label18.place(x=970, y=500)
    # global pcodeEntry
    pcodeEntry = Entry(croot, width=10)
    pcodeEntry.place(x=1020, y=500)
    labels = [ label11, label12, label13, label14, label15, label16, label17, label18 ]
    Updatebutton = tkinter.Button(croot, text="Add",
                                  command=lambda: CUpdateDatabase(idEntry, nameEntry, surnameEntry, emailEntry, phoneEntry,
                                                           addressEntry, cityEntry, pcodeEntry, labels, Updatebutton))
    Updatebutton.place(x=1070, y=500)


def CDeleteDatabase(idEntry, label11,deletebutton):
    print(idEntry.get())
    Capp.delete(idEntry.get())
    idEntry.place_forget()
    label11.place_forget()
    deletebutton.place_forget()

# Delete Page
def CDeletePage():
    # ID
    label11 = tk.Label(croot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(croot, width=10)
    idEntry.place(x=40, y=500)
    deletebutton = tkinter.Button(croot, text="Delete",
                                  command=lambda: CDeleteDatabase(idEntry, label11,
                                                                 deletebutton))
    deletebutton.place(x=100, y=500)

def MainCustomer():
    global Capp
    Capp= App()
    global croot
    croot= Capp.Root()

    label1 = tkinter.Label(croot, text="Search", font=("straight", 11, "bold"))
    label1.place(x=10, y=526)

    entry = Entry(croot, width=20)
    entry.place(x=100, y=526)

    button = tkinter.Button(croot, text="Search", command=lambda : CSearch(entry))
    button.place(x=250, y=526)

    bt1 = tk.Button(croot, text='Add Form', command=CAddPage)
    bt1.place(x=310, y=526)

    bt2 = tk.Button(croot, text='update Form', command=CUpdatePage)
    bt2.place(x=390, y=526)

    bt3 = tk.Button(croot, text='Delete Form', command=CDeletePage)
    bt3.place(x=485, y=526)
    Capp.mainloop()

    # Main()
    list1 = [ 1, 'has', 'baig', 'i18021@gmail.com', '03041231433', 'near capital', 'pes', 'Z100' ]
    list2 = [ 2, 'Vishi', 'SAI', 'i18021@gmail.com', '03241231433', 'near capital', 'isl', 'Z100' ]
    list3 = [ 'Vishi', 'SAI', 'i18021@gmail.com', '03241231433', 'near capital', 'isl', 'Z100', 2 ]

    # # app.add(list1)
    # # app.add(list2)
    # # app.add(list3)
    # # app.update(list3)
    # # app.delete(2)


# MainCustomer()