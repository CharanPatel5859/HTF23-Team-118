#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import random
from twilio.rest import Client


# In[2]:


import sqlite3
import random
from twilio.rest import Client

# Function to create the scheduling database with 15 tables
def create_scheduling_database():
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    
    # Create 15 tables (tb1, tb2, ..., tb15)
    for i in range(1, 16):
        table_name = f'tb{i}'
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            due_date TEXT,
            status TEXT
        )
        '''
        cursor.execute(create_table_query)

    # Create the "users" table for user registration
    create_users_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        password TEXT
    )
    '''
    cursor.execute(create_users_table_query)
    
    conn.commit()
    conn.close()

# Function to generate a random 4-digit password
def generate_password():
    return str(random.randint(1000, 9999))

# Function to send an SMS using Twilio
def send_sms(to_phone_number, message):
    # Twilio credentials
    account_sid = "ACa7c39a50618f0cc2fd11d0f785b9c83f"
    auth_token = "ba316917c20a09b1dd6854c0d881629a"
    twilio_phone_number = +17792464751

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )

# Function for user registration
def register_user():
    phone_number = input("Enter your phone number (e.g., +1234567890): ")

    # Check if the user is already registered
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    check_user_query = "SELECT * FROM users WHERE phone_number = ?"
    cursor.execute(check_user_query, (phone_number,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("You are already registered. Please log in.")
        conn.close()
        return

    # Generate a random 4-digit password
    password = generate_password()

    # Insert user into the database
    insert_user_query = "INSERT INTO users (phone_number, password) VALUES (?, ?)"
    cursor.execute(insert_user_query, (phone_number, password))
    conn.commit()
    conn.close()

    # Send the password via SMS
    send_sms(phone_number, f"Your registration password: {password}")
    print("Registration successful! Check your SMS for the password.")

# Function for user login
def login_user():
    phone_number = input("Enter your phone number (e.g., +1234567890): ")
    password = input("Enter your 4-digit password: ")

    # Check if the user exists and the password is correct
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    check_user_query = "SELECT * FROM users WHERE phone_number = ? AND password = ?"
    cursor.execute(check_user_query, (phone_number, password))
    existing_user = cursor.fetchone()
    
    

    if existing_user:
        print("Login successful!")
        user_table = f'tb{existing_user[0]}'  # Assuming user's ID is used for table name
        print(f"YOUR TABLE IS {user_table}")
        manage_table(user_table)
    else:
        print("Login failed. Please check your phone number and password and then try again or YOU MAY NOT BE REGISTERED ")
    conn.close()

# Function to manage a user's table
def manage_table(user_table):
    while True:
        print(f"\nOptions for {user_table}:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Display Tasks")
        print("4. Edit Task (Due Date and Status)")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            
            task = input("Enter task: ")
            due_date = input("Enter due date: ")
            
            status = input("Enter status: ")
            add_task(user_table, task, due_date, status)

        elif choice == '2':
            task_id = input("Enter task ID to delete: ")
            delete_task(user_table, task_id)

        elif choice == '3':
            display_tasks(user_table)

        elif choice == '4':
            task_id = input("Enter task ID to edit: ")
            new_due_date = input("Enter new due date: ")
            new_status = input("Enter new status: ")
            edit_task(user_table, task_id, new_due_date, new_status)

        elif choice == '5':
            print("Logout successful!")
            break

# Function to add a task
def add_task(user_table, task, due_date, status):
    print("YOUR TASKS ARE:-")
    display_tasks(user_table)
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    insert_query = f"INSERT INTO {user_table} (task, due_date, status) VALUES (?, ?, ?)"
    cursor.execute(insert_query, (task, due_date, status))
    conn.commit()
    conn.close()
    print("Task added successfully!")

# Function to delete a task by ID
def delete_task(user_table, task_id):
    print("YOUR TASKS ARE:-")
    display_tasks(user_table)
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    delete_query = f"DELETE FROM {user_table} WHERE rowid = ?"
    cursor.execute(delete_query, (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

# Function to display all tasks
def display_tasks(user_table):
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    select_query = f"SELECT rowid, task, due_date, status FROM {user_table}"
    cursor.execute(select_query)
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        print("\nTasks:")
        for task in tasks:
            print(task)  # Now includes task IDs
    else:
        print("No tasks found.")

# Function to edit due date and status by ID
def edit_task(user_table, task_id, new_due_date, new_status):
    print("YOUR TASKS ARE:-")
    display_tasks(user_table)
    
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()
    update_query = f"UPDATE {user_table} SET due_date = ?, status = ? WHERE rowid = ?"
    cursor.execute(update_query, (new_due_date, new_status, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully!")

# Main function
def main():
    create_scheduling_database()
    
    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()


# In[18]:


phone_number = input("Enter your phone number (e.g., +1234567890): ")
password = str(input("Enter your 4-digit password: "))

    # Check if the user exists and the password is correct
conn = sqlite3.connect('scheduling.db')
cursor = conn.cursor()
check_user_query = "SELECT * FROM users WHERE phone_number = ? AND password = ?"
cursor.execute(check_user_query, (phone_number, password))
existing_user = cursor.fetchone()
if existing_user[2]==password:
    print("hdfkjhskf")
print(existing_user)
    


# In[10]:





# In[ ]:




