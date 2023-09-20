import tkinter as tk
from tkinter import ttk, PhotoImage
import pymysql

def execute_sql_query():
    connection_name = connection_name_entry.get()
    server = server_entry.get()
    port = port_entry.get()
    database_name = database_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    try:
        if not server or not port or not connection_name:
            connection_status_label.config(text="Please enter all required information.")
            return

        connection_string = f"host={server}, port={port}, user={username}, password={password}, db={database_name}"

        connection = pymysql.connect(host=server, port=int(port), user=username, password=password, database=database_name)
        cursor = connection.cursor()

        if connection:
            connection_status_label.config(text=f"Connected to '{connection_name}' database successfully.")
            
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            table_combobox['values'] = [table[0] for table in tables]
        else:
            connection_status_label.config(text="Failed to connect to the database.")

        connection.close()
    except Exception as e:
        connection_status_label.config(text=f"Error: {str(e)}")

def view_selected_table():
    selected_table = table_combobox.get()
    if selected_table:
        try:
            connection = pymysql.connect(host=server_entry.get(), port=int(port_entry.get()), user=username_entry.get(), password=password_entry.get(), database=database_name_entry.get())
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {selected_table};")
            table_data = cursor.fetchall()

            table_text.delete(1.0, tk.END)

            for row in table_data:
                table_text.insert(tk.END, ', '.join(map(str, row)) + "\n")
        except Exception as e:
            connection_status_label.config(text=f"Error: {str(e)}")
    else:
        connection_status_label.config(text="Please select a table.")

root = tk.Tk()
root.title("DataNav")

icon = PhotoImage(file="DV.png")
root.iconphoto(True, icon)

connection_name_label = tk.Label(root, text="Connection name:")
connection_name_label.pack()
connection_name_entry = tk.Entry(root, width=50)
connection_name_entry.pack()

server_label = tk.Label(root, text="Server Address:")
server_label.pack()
server_entry = tk.Entry(root, width=50)
server_entry.pack()

port_label = tk.Label(root, text="Port:")
port_label.pack()
port_entry = tk.Entry(root, width=50)
port_entry.pack()

database_name_label = tk.Label(root, text="Database:")
database_name_label.pack()
database_name_entry = tk.Entry(root, width=50)
database_name_entry.pack()

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root, width=50)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, width=50, show="*")
password_entry.pack()

execute_button = tk.Button(root, text="Connect and Get Tables", command=execute_sql_query)
execute_button.pack()

connection_status_label = tk.Label(root, text="")
connection_status_label.pack()

table_combobox_label = tk.Label(root, text="Select Table:")
table_combobox_label.pack()
table_combobox = ttk.Combobox(root, width=50)
table_combobox.pack()

view_table_button = tk.Button(root, text="View Table Data", command=view_selected_table)
view_table_button.pack()

table_text_label = tk.Label(root, text="Table Data:")
table_text_label.pack()
table_text = tk.Text(root, height=10, width=80)
table_text.pack()

root.mainloop()
