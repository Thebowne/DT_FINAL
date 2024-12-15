from tkinter import *
import mysql.connector
from mysql.connector import Error


# MySQL to Python connection
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def read_data(connection, table):
    cursor = connection.cursor()
    query = f"SELECT * FROM gym_management.{table};"
    results = []
    column_names = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
    return results, column_names


def populate_treeview(data, column_names):

    for widget in content_frame.winfo_children():
        widget.destroy()

    header = Label(content_frame, text=" | ".join(column_names), font=("Arial", 10, "bold"))
    header.pack(fill=BOTH,  expand=True)

    for row in data:
        row_data = " | ".join(str(item) for item in row)
        Label(content_frame, text=row_data, font=("Arial", 10)).pack(fill=BOTH, expand=True)


# View button usage
def on_view_button_click():
    table = selected_option.get()
    conn = create_connection('localhost', 'root', 'D4bst3as_', 'gym_management')
    if conn and table != "-Select-":
        data, column_names = read_data(conn, table)
        populate_treeview(data, column_names)
        conn.close()


# For Dropdown List
def show_selection(value):
    label.config(text=f"You selected: {value}")


def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


# Window size
windows = Tk()
windows.title('Fitness Center Database Management')
windows.geometry('1280x720+200+10')
windows.resizable(True, True)


# Frame A
frame_a = Frame(windows, bg='#B896EB', bd=8, height=80)
frame_a.pack(side=TOP, fill=X)
frame_a.pack_propagate(False)

captionlbl = Label(frame_a,
                   text='Gym Database Management System',
                   font=("Inter", 28 * -1),
                   bg='#B896EB')
captionlbl.pack(fill=BOTH, expand=True)


# Frame B
frame_b = Frame(windows, bg='#F8F6FF',padx=80, pady=40)
frame_b.pack(side=LEFT, fill=Y)
frame_b.pack_propagate(False)

userlbl = Label(frame_b, text='User: Admin', bg='#F8F6FF')
userlbl.grid(row=0, column=0, sticky='nsew', pady=10)

plcholder = Label(frame_b, text='').grid(row=1, column=0)

selected_option = StringVar(frame_b)
selected_option.set("-Select-")  # Default option

# Options for the dropdown
options = ["Booking", "Classes", "Enrollment", "Equipment", "Members", "MembershipType", "Staff", "StaffSchedule"]

# Dropdown list for tables
dropdown = OptionMenu(frame_b, selected_option, *options, command=show_selection)
dropdown.config(font=('Calibre', 12, 'bold'))
dropdown.grid(row=3, column=0, pady=10)

label = Label(frame_b, text=f"You selected: {selected_option.get()}")
label.grid(row=2, column=0, pady=10)

btn1 = Button(frame_b, text='View', width=15, height=2, font=('Calibre', 12, 'bold'),
              command=on_view_button_click)
btn1.grid(row=4, column=0, pady=10)

btn2 = Button(frame_b, text='Add', width=15, height=2, font=('Calibre', 12, 'bold'))
btn2.grid(row=5, column=0, pady=10)

btn3 = Button(frame_b, text='Update', width=15, height=2, font=('Calibre', 12, 'bold'))
btn3.grid(row=6, column=0, pady=10)

btn4 = Button(frame_b, text='Delete', width=15, height=2, font=('Calibre', 12, 'bold'))
btn4.grid(row=7, column=0, pady=10)


# Frame C
frame_c = Frame(windows, bg='#e6e4e1', padx=70, pady=70)
frame_c.pack(fill=BOTH, expand=True)

canvas = Canvas(frame_c, bg='white')
canvas.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(canvas, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

content_frame.bind("<Configure>", on_canvas_configure)

scrollbar.config(command=canvas.yview)

windows.mainloop()
