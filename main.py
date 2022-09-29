import tkinter as tk

r = tk.Tk()
r.geometry('300x250')
r.title('Appointment Booking System')


def Cpage():
    import customer
    customer.MainCustomer()


def Bpage():
    import booking
    booking.MainBooking()


def Jpage():
    import job
    job.MainJob()


button1 = tk.Button(r, text='Customer Table', width=25, command=Cpage)
button2 = tk.Button(r, text='Booking Table', width=25, command=Bpage)
button3 = tk.Button(r, text='Job Table', width=25, command=Jpage)
button4 = tk.Button(r, text='Quit', width=25, command=r.destroy)
button1.place(x=30, y=30)
button2.place(x=30, y=70)
button3.place(x=30, y=110)
button4.place(x=30, y=150)

r.mainloop()
