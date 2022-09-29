import tkinter.messagebox
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *
from tkinter import Entry
import tkinter as tk
from tkcalendar import DateEntry


class Job(tk.Tk):
    def __init__(self):
        super( ).__init__( )

        self.title('Appointment System')
        self.geometry('1500x600')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tree = self.create_tree_widget( )

    def Root(self):
        return self.tree

    def create_tree_widget(self):
        columns = ('Job_id', 'Type', 'Desc', 'Job_start', 'Job_finished')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('Job_id', text='Job_id')
        tree.heading('Type', text='Type')
        tree.heading('Desc', text='Desc')
        tree.heading('Job_start', text='Job_start')
        tree.heading('Job_finished', text='Job_finished')

        tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # generate sample data

        conn = None
        conn = connect("Job.db")
        curs = conn.cursor( )
        db = """create table IF NOT EXISTS  Job(Job_id INT PRIMARY KEY, Type TEXT, Desc TEXT, Job_start TEXT,
        Job_finished TEXT); """

        curs.execute(db)
        conn.commit( )

        # add data to the treeview
        curs.execute("SELECT * FROM Job")
        rows = curs.fetchall( )
        conn.close( )

        for row in rows:
            tree.insert('', tk.END, values=row)

        return tree

    def item_selected(self, event):
        for selected_item in self.tree.selection( ):
            item = self.tree.item(selected_item)
            record = item[ 'values' ]
            # show a message
            tkinter.messagebox.showinfo(title='Information', message=','.join(record))

    def add(self, attrs):
        conn = connect("Job.db")
        curs = conn.cursor( )
        data_tuple = tuple(attrs)
        query1 = '''INSERT OR IGNORE INTO Job(Type, Desc, Job_start, Job_finished) VALUES(?,?,?,?);'''

        curs.execute(query1, data_tuple)
        conn.commit( )

        # add data to the treeview
        curs.execute("SELECT * FROM Job")
        rows = curs.fetchall( )
        conn.close( )

        self.tree.insert('', tk.END, values=rows[ -1 ])
        conn.close( )

    def update(self, attrs):
        conn = connect("Job.db")
        curs = conn.cursor( )
        update_tuple = tuple(attrs)
        query1 = '''update Job set Type = ?, Desc = ?, Job_start = ?,
        Job_finished = ? where Job_id = ? '''

        curs.execute(query1, update_tuple)
        conn.commit( )
        self.tree.place_forget( )
        # add data to the treeview
        curs.execute("SELECT * FROM Job")
        rows = curs.fetchall( )
        conn.close( )
        for i in self.tree.get_children( ):
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def delete(self, id):
        conn = connect("Job.db")
        curs = conn.cursor( )
        query1 = '''delete from Job where Job_id = ?'''

        curs.execute(query1, (id,))
        conn.commit( )
        self.tree.place_forget( )
        # add data to the treeview
        curs.execute("SELECT * FROM Job")
        rows = curs.fetchall( )
        conn.close( )
        for i in self.tree.get_children( ):
            self.tree.delete(i)

        for row in rows:
            self.tree.insert('', tk.END, values=row)


def JSearch(entry):
    # self.tree.selection()
    name = entry.get( )
    print(name)
    jroot.selection( )
    fetchdata = jroot.get_children( )
    for f in fetchdata:
        jroot.delete(f)
    conn = None
    try:
        conn = connect("job.db")
        core = conn.cursor( )
        db = "select * from Job where Job_id = '%s' "
        name = entry.get( )
        if (len(name) < 0):
            showerror("fail", "invalid name")
        else:
            core.execute(db % (name))
            data = core.fetchall( )
            for d in data:
                jroot.insert("", tk.END, values=d)

    except Exception as e:
        showerror("issue", e)

    finally:
        if conn is not None:
            conn.close( )


def JAddDatabase(typeEntry, descEntry, jobstartEntry, jobfinishedEntry,
                 labels, Addbutton):
    # Adding into list
    attributes = list( )
    attributes.append(typeEntry.get( ))
    attributes.append(descEntry.get( ))
    attributes.append(jobstartEntry.get( ))
    attributes.append(jobfinishedEntry.get( ))
    print(attributes)
    jobapp.add(attributes)
    typeEntry.place_forget( )
    descEntry.place_forget( )
    jobstartEntry.place_forget( )
    jobfinishedEntry.place_forget( )
    for label in labels:
        label.place_forget( )
    Addbutton.place_forget( )


def JAddPage():

    # type
    label14 = tk.Label(jroot, text='Type')
    label14.place(x=110, y=500)
    typeEntry = Entry(jroot, width=12)
    typeEntry.place(x=150, y=500)

    # Desc
    label15 = tk.Label(jroot, text='Desc')
    label15.place(x=230, y=500)
    # global emailEntry
    descEntry = Entry(jroot, width=12)
    descEntry.place(x=270, y=500)
    #
    # job start
    label12 = tk.Label(jroot, text='Job Start')
    label12.place(x=355, y=500)
    # nameEntry = Entry(jroot, width=10)
    jobstartEntry = DateEntry(jroot, selectmode='day', textvariable=jobstartstring)
    jobstartEntry.place(x=420, y=500)
    #
    # Finished
    label13 = tk.Label(jroot, text='Job Finished')
    label13.place(x=520, y=500)
    # nameEntry = Entry(jroot, width=10)
    jobfinishedEntry = DateEntry(jroot, selectmode='day', textvariable=jobfinishedstring)
    jobfinishedEntry.place(x=600, y=500)

    labels = [ label12, label13, label14, label15 ]
    Addbutton = tkinter.Button(jroot, text="Add",
                               command=lambda: JAddDatabase(typeEntry, descEntry, jobstartEntry,
                                                            jobfinishedEntry,
                                                            labels, Addbutton))
    Addbutton.place(x=700, y=500)


def JUpdateDatabase(idEntry, typeEntry, descEntry, jobstartEntry, jobfinishedEntry,
                    labels, Addbutton):
    # Adding into list
    attributes = list( )
    attributes.append(typeEntry.get( ))
    attributes.append(descEntry.get( ))
    attributes.append(jobstartEntry.get( ))
    attributes.append(jobfinishedEntry.get( ))
    attributes.append(idEntry.get( ))

    print(attributes)
    jobapp.update(attributes)
    typeEntry.place_forget( )
    descEntry.place_forget( )
    jobstartEntry.place_forget( )
    jobfinishedEntry.place_forget( )
    idEntry.place_forget( )
    for label in labels:
        label.place_forget( )
    Addbutton.place_forget( )


def JUpdatePage():
    # ID
    label11 = tk.Label(jroot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(jroot, width=10)
    idEntry.place(x=40, y=500)

    # type
    label14 = tk.Label(jroot, text='Type')
    label14.place(x=110, y=500)
    typeEntry = Entry(jroot, width=12)
    typeEntry.place(x=150, y=500)

    # Desc
    label15 = tk.Label(jroot, text='Desc')
    label15.place(x=230, y=500)
    # global emailEntry
    descEntry = Entry(jroot, width=12)
    descEntry.place(x=270, y=500)
    #
    # job start
    label12 = tk.Label(jroot, text='Job Start')
    label12.place(x=355, y=500)
    # nameEntry = Entry(jroot, width=10)
    jobstartEntry = DateEntry(jroot, selectmode='day', textvariable=jobstartstring)
    jobstartEntry.place(x=420, y=500)
    #
    # Finished
    label13 = tk.Label(jroot, text='Job Finished')
    label13.place(x=520, y=500)
    # nameEntry = Entry(jroot, width=10)
    jobfinishedEntry = DateEntry(jroot, selectmode='day', textvariable=jobfinishedstring)
    jobfinishedEntry.place(x=600, y=500)

    labels = [ label11, label12, label13, label14, label15 ]
    Addbutton = tkinter.Button(jroot, text="Add",
                               command=lambda: JUpdateDatabase(idEntry, typeEntry, descEntry, jobstartEntry,
                                                               jobfinishedEntry,
                                                               labels, Addbutton))
    Addbutton.place(x=700, y=500)


def JDeleteDatabase(idEntry, label11, deletebutton):
    print(idEntry.get( ))
    jobapp.delete(idEntry.get( ))
    idEntry.place_forget( )
    label11.place_forget( )
    deletebutton.place_forget( )


# Delete Page
def JDeletePage():
    # ID
    label11 = tk.Label(jroot, text='Id')
    label11.place(x=10, y=500)
    # global idEntry
    idEntry = Entry(jroot, width=10)
    idEntry.place(x=40, y=500)
    deletebutton = tkinter.Button(jroot, text="Delete",
                                  command=lambda: JDeleteDatabase(idEntry, label11,
                                                                  deletebutton))
    deletebutton.place(x=100, y=500)


def MainJob():
    global jobapp
    jobapp = Job( )

    jList1 = [ 1, 'online', 'computer scientist', '12/12/12', '12/4/15' ]
    jList2 = [ 2, 'onsite', 'engineer', '12/12/12', '12/4/15' ]

    global jobstartstring
    jobstartstring = tkinter.StringVar( )  # declaring string variable
    global jobfinishedstring
    jobfinishedstring = tkinter.StringVar( )  # declaring string variable

    updateJList2 = [ 'online', 'astronaut', '12/11/12', '12/4/19', 2 ]

    # jobapp.add(jList1)
    # jobapp.add(jList2)
    # jobapp.update(updateJList2)
    # jobapp.delete(2)

    global jroot
    jroot = jobapp.Root( )

    label1 = tkinter.Label(jroot, text="Search", font=("straight", 11, "bold"))
    label1.place(x=10, y=526)

    entry = Entry(jroot, width=20)
    entry.place(x=100, y=526)

    button = tkinter.Button(jroot, text="Search", command=lambda: JSearch(entry))
    button.place(x=250, y=526)

    bt1 = tk.Button(jroot, text='Add Form', command=JAddPage)
    bt1.place(x=310, y=526)

    bt2 = tk.Button(jroot, text='update Form', command=JUpdatePage)
    bt2.place(x=390, y=526)

    bt3 = tk.Button(jroot, text='Delete Form', command=JDeletePage)
    bt3.place(x=485, y=526)

    jobapp.mainloop( )

# MainJob()
