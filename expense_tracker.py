import tkinter as tk
from tkinter import ttk, messagebox
from mydb import Database

# Initialize the database
db = Database('expenses.db')

# Create the main window
window = tk.Tk()
window.title("Expense Tracker")
window.geometry("800x600+300+100")

# Functions
def load_records():
    tree.delete(*tree.get_children())  # Clear the treeview
    for row in db.fetch_records():  # Fetch records from the database
        tree.insert("", tk.END, values=row)  # Insert them into the treeview

def save_record():
    item_name = item_name_entry.get()
    item_price = item_price_entry.get()
    purchase_date = purchase_date_entry.get()

    if item_name and item_price and purchase_date:
        try:
            item_price = float(item_price)  # Ensure item_price is a valid float
            db.insert_record(item_name, item_price, purchase_date)
            load_records()
            clear_entry()
            status_label.config(text="Record saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid price value. Enter a number.")
    else:
        messagebox.showerror("Error", "All fields are required.")

def delete_record():
    selected_item = tree.selection()
    if selected_item:
        record_id = tree.item(selected_item[0], "values")[0]  # Get the ID from the selected row
        try:
            db.remove_record(record_id)  # Use ID to delete
            load_records()  # Reload records
            status_label.config(text="Record deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")
    else:
        messagebox.showerror("Error", "Please select a record to delete.")

def update_entry():
    selected_item = tree.selection()
    if selected_item:
        record_id = tree.item(selected_item[0], "values")[0]  # Get the ID
        item_name = item_name_entry.get()
        item_price = item_price_entry.get()
        purchase_date = purchase_date_entry.get()

        if item_name and item_price and purchase_date:
            try:
                db.update_record(record_id, item_name, float(item_price), purchase_date)
                load_records()  # Reload records
                clear_entry()  # Clear entry fields
                status_label.config(text="Record updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid price value. Enter a number.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update record: {e}")
        else:
            messagebox.showerror("Error", "All fields are required.")
    else:
        messagebox.showerror("Error", "Please select a record to update.")

def total_balance():
    try:
        total = sum([float(row[2]) for row in db.fetch_records()])
        messagebox.showinfo("Total Balance", f"Total Balance: ${total:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate total balance: {e}")

def clear_entry():
    item_name_entry.delete(0, tk.END)
    item_price_entry.delete(0, tk.END)
    purchase_date_entry.delete(0, tk.END)

def exit_app():
    window.destroy()

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item[0], "values")
        if len(values) == 4:  # Ensure the row has all columns
            item_name_entry.delete(0, tk.END)
            item_name_entry.insert(0, values[1])
            item_price_entry.delete(0, tk.END)
            item_price_entry.insert(0, values[2])
            purchase_date_entry.delete(0, tk.END)
            purchase_date_entry.insert(0, values[3])

# UI Elements
entry_label = tk.Label(window, text="Add New Expense", font=('Arial', 14, 'bold'))
entry_label.pack(pady=(10, 0))

# Top Frame
top_frame = tk.Frame(window)
top_frame.pack(pady=10)

# Left frame (entries)
left_frame = tk.Frame(top_frame)
left_frame.pack(side="left", padx=20)

tk.Label(left_frame, text="Item Name:").pack(anchor="w")
item_name_entry = tk.Entry(left_frame, width=30)
item_name_entry.pack()

tk.Label(left_frame, text="Item Price:").pack(anchor="w")
item_price_entry = tk.Entry(left_frame, width=30)
item_price_entry.pack()

tk.Label(left_frame, text="Purchase Date (YYYY-MM-DD):").pack(anchor="w")
purchase_date_entry = tk.Entry(left_frame, width=30)
purchase_date_entry.pack()

# Right frame (buttons)
right_frame = tk.Frame(top_frame)
right_frame.pack(side="right", padx=20)

button_config = {'width': 12, 'height': 2, 'font': ('Arial', 12, 'bold')}
tk.Button(right_frame, text="Save Record", command=save_record, **button_config).grid(row=0, column=0, padx=5, pady=5)
tk.Button(right_frame, text="Clear Entry", command=clear_entry, **button_config).grid(row=0, column=1, padx=5, pady=5)
tk.Button(right_frame, text="Delete Entry", command=delete_record, **button_config).grid(row=1, column=0, padx=5, pady=5)
tk.Button(right_frame, text="Update Entry", command=update_entry, **button_config).grid(row=1, column=1, padx=5, pady=5)
tk.Button(right_frame, text="Total Balance", command=total_balance, **button_config).grid(row=2, column=0, padx=5, pady=5)
tk.Button(right_frame, text="Exit", command=exit_app, **button_config).grid(row=2, column=1, padx=5, pady=5)

# Table for Expense Records
table_label = tk.Label(window, text="Expense Records", font=('Arial', 14, 'bold'))
table_label.pack(pady=(10, 0))

bottom_frame = tk.Frame(window)
bottom_frame.pack(padx=20, pady=20, fill="both", expand=True)

columns = ("ID", "Item Name", "Item Price", "Purchase Date")
tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(side="left", fill="both", expand=True)
scrollbar = tk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Status bar
status_label = tk.Label(window, text="Ready", bd=1, relief="sunken", anchor="w")
status_label.pack(side="bottom", fill="x")

# Load records initially
load_records()

# Run the application
window.mainloop()
