import sqlite3
import re


import hashlib
from getpass import getpass
menu = """
1. Sign Up
2. Log In
3. Exit
"""



def connect_to_db():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    return cursor, conn


def set_up():
    cursor, _ = connect_to_db()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS bankss(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        amount REAL NOT NULL
    )
        """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS transactionnn(
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        username TEXT NOT NULL,
        type TEXT NOT NULL,
        amount REAL
       
    )
        """
    )



def create_user(full_name, username, password,amount):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor, conn = connect_to_db()
    try:
        cursor.execute(
            """
            INSERT INTO bankss(full_name, username, password,amount)
            VALUES (?,?,?,?)
            """, (full_name,username,hashed_password,amount)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("The username already exists")
    else:
        print("Account created succesfully")
    finally:
        conn.close()

def sign_up():
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    while True:
        amount=0
        full_name = input("Enter your full name: ")
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        confirm_password = getpass("Confirm your password")
        try:
            initial_deposit = int(input("Enter your initial deposit: "))
        except ValueError:
            print("Invalid input")
            continue
        cursor.execute('INSERT INTO transactionnn(username, type, amount) VALUES (?, ?, ?)',(username, 'Deposit', initial_deposit))
        conn.commit()
        amount += initial_deposit
       
        if not full_name:
            print("Full name cannot be empty")
            continue
        if len(full_name) < 4:
            print("Full name must be at least 4 character")
            continue
        if len(full_name) >255:
            print("Full name is too long")
            continue

        if not username:
            print("Username cannot be empty")
            continue

        if len(username) < 3:
            print("Username is too small")
            continue
        if len(username) >20:
            print("Username is too long")
            continue
        
        if not password:
            print("Password field is required")
            continue

        if not confirm_password:
            print("Confirm password cannot be blank")
            continue
        if password != confirm_password:
            print("Those two password don't match")
            continue

        passworrd_pattern= r"[A-Za-z0-9!@#$%^&*(),.?\":{}]"
        valid = re.search(passworrd_pattern,password)
        if len(password) < 8 or not valid:
            print("Invalid password,include uppercase, lowercase and a special character")
            continue

        if len(password) <8:
            print("Password is too short")
            continue

        
        if initial_deposit< 2000:
            print("Minimum deposit is 2000")
            continue
        break
    
    create_user(full_name,username,password,amount)


session = {}
def create_session(username):
    print("Welcome back",username)
    session[username] = True

def log_in(username)
    password = getpass("Enter your password: ").strip()
    while True:
        if not username:
            print("Username cannot be blank")
            continue
        if not password:
            print("Password cannot be blank")
            continue
        break
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor, conn = connect_to_db()

    cursor.execute(
        """
    SELECT * FROM bankss
    WHERE username = ? AND password = ?
        """,(username,hashed_password)
    )
    user = cursor.fetchone()
    if user:
        print("Login Successful")
        create_session(username)
    else:
        print("Incorrect details, wrong username or password")   
    conn.close()
    return username




def deposit(username):
    while True:
        try:
            amount = int(input("Enter your deposit amount: "))
        except ValueError:
            print("Invalid input")
            continue

        if not username:
            print("Username cannot be empty")
            continue

        if not amount:
            print("Amount cannot be empty")
            continue

        if amount < 0:
            print("Amount cannot be negative")
            continue
        break
        
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bankss SET amount = amount + ? WHERE username = ?', (amount, username))
    cursor.execute('INSERT INTO transactionnn(username, type, amount) VALUES (?, ?, ?)',(username, 'Deposit', amount))
    conn.commit()
    cursor.execute("SELECT amount FROM bankss WHERE username = ?",(username,))
    amountt = cursor.fetchone()
    print(f"Deposited {amount} successfully!")
    print("Your new balance is",amountt)
    cursor.execute("SELECT * FROM bankss")
    # m = cursor.fetchall()
    # print(m)
    conn.close()

   


    
def withdraw(username):
    while True:
        username=input("Enter your username: ")
        try:
            amount = int(input("Enter the amount you want to withdraw: "))
        except ValueError:
            print("Invalid input")
            continue
        if not amount:
            print("Amount cannot be empty")
            continue

        if amount < 0:
            print("Amount cannot be negative")
            continue
        break
        
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM bankss WHERE username = ?', (username,))
    try:
        balance = cursor.fetchone()[0]
    except TypeError:
        print("Username does not exist")
    else:
        if balance >= amount:
    
            cursor.execute('UPDATE bankss SET amount = amount - ? WHERE username = ?', (amount, username))
            cursor.execute('INSERT INTO transactionnn(username, type, amount) VALUES (?, ?, ?)',(username, 'Withdraw', amount))
            conn.commit()
            cursor.execute("SELECT amount FROM bankss WHERE username = ?",(username,))
            amountt = cursor.fetchone()
            print(f"Withdrawal of {amount} successfully!")
            print("Your balance is new",amountt)
        else:
            print("Insufficient fund")
    finally:
        conn.close()
    # m = cursor.fetchall()
    # print(m)
    conn.close()

def check_balance(username):
    username = input("Enter your username: ")
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM bankss WHERE username = ?', (username,))
    try:
        balance = cursor.fetchone()[0]
        print("Your balance is", balance)
    except TypeError:
        print("Username does not exist")
    else:
        print(f"Your current balance is: {balance}")
    finally:
        conn.close()
def transfer(username):
    while True:
        recipient = input("Enter recipient username: ")
        if username == recipient:
            print("Self-transfer is not allowed")
            continue
        break
    amount = int(input("Enter amount: "))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM bankss WHERE username = ?', (username,))
    try:
        sender_balance = cursor.fetchone()[0]
    except TypeError:
        print("Username does not exist")
    else:
        if sender_balance >= amount:
            cursor.execute('UPDATE bankss SET amount = amount - ? WHERE username = ?', (amount, username))
            cursor.execute('UPDATE bankss SET amount = amount + ? WHERE username = ?', (amount, recipient))
            cursor.execute('INSERT INTO transactionnn(username, type, amount) VALUES (?, ?, ?)',(username, 'Transfer', amount))
            cursor.execute('INSERT INTO transactionnn(username, type, amount) VALUES (?, ?, ?)',(recipient, 'Recieve', amount))
            conn.commit()
            print(f"{amount} transferred successfully!")
        else:
            print("Insufficient balance.")
    finally:
        conn.close()
def is_logged_in(username):
    return session.get(username,False)

def transaction_history(username):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactionnn WHERE username = ?', (username,))
    transactions = cursor.fetchall()
    if len(transactions) == 0:
        print("No transaction yet!")
    for rows in transactions:
        print(rows)
    conn.close()

def main():
    set_up()
    while True:
        print(menu)
        choice = input("Enter your choice: ")
        if choice == "3":
            break
        elif choice == "1":
            sign_up()
        elif choice == "2":
            username = input("Enter username: ")
            log_in(username)

            if is_logged_in(username):
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transfer")
                    print("5. transaction history ")
                    print("6. Exit")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        deposit(username)
                    elif user_choice == "2":
                        withdraw(username)
                    elif user_choice == "3":
                        check_balance(username)
                   
                    elif user_choice == "4":
                        transfer(username)
                    elif user_choice == "5":
                        transaction_history(username)
                    elif user_choice == "6":
                        break
                    else:
                        print("Invalid choice!")
        else:
            print("Invalid choice!")
main()