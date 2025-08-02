import mysql.connector
import requests

# === Configuration ===
API_KEY = "YOUR_RAPIDAPI_KEY_HERE " 

# === Database Connection ===
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='YourRootPasswordHere',  # Replace
        database='railways'
    )

# === Sign In ===
def signin():
    p = input("System password: ")
    if p == "YourRootPasswordHere":  # Replace
        options()
    else:
        print("Incorrect password.")
        signin()

# === Menu Options ===
def options():
    print("\n--- Railway Booking System ---")
    print("1. Add Train")
    print("2. Book Train")
    print("3. Add Customer")
    print("4. Display Trains")
    print("5. Display Customers")
    print("6. Display Bills")
    print("7. Get Live Location")
    print("8. Check Seat Availability")
    print("9. Exit")

    try:
        value = int(input("Enter option number: "))
    except ValueError:
        print("Please enter a number.")
        return options()

    if value == 1:
        add_train()
    elif value == 2:
        book_train()
    elif value == 3:
        add_customer()
    elif value == 4:
        display_trains()
    elif value == 5:
        display_customers()
    elif value == 6:
        display_bills()
    elif value == 7:
        get_live_location()
    elif value == 8:
        check_seat_availability()
    elif value == 9:
        print("Exiting...")
        exit()
    else:
        print("Invalid option.")
        options()

# === Add Train ===
def add_train():
    conn = get_connection()
    cursor = conn.cursor()
    date_of_arrival = input("Date of arrival (YYYY-MM-DD): ")
    name_of_train = input("Train name: ")
    cost = int(input("Cost: "))
    distance = int(input("Distance travelled: "))
    source = input("Source station: ")
    destination = input("Destination station: ")
    location = input("Current location (optional): ")

    sql = """
    INSERT INTO train 
    (date_of_arrival, name_of_train, cost, distance_travelled, source_station, destination_station, current_location)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (date_of_arrival, name_of_train, cost, distance, source, destination, location))
        conn.commit()
        print("Train added successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
        options()

# === Book Train ===
def book_train():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name_of_train FROM train")
        trains = cursor.fetchall()
        print("\nAvailable Trains:")
        for train in trains:
            print("-", train[0])
        selected = input("Enter train name to book: ")
        cursor.execute("SELECT cost, date_of_arrival FROM train WHERE name_of_train = %s", (selected,))
        result = cursor.fetchone()
        if result:
            cost, doa = result
            cursor.execute("INSERT INTO bills (train_booked, cost, date_of_arrival) VALUES (%s, %s, %s)",
                           (selected, cost, doa))
            conn.commit()
            print("Train booked successfully.")
        else:
            print("Train not found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
        options()

# === Add Customer ===
def add_customer():
    conn = get_connection()
    cursor = conn.cursor()
    name = input("Customer name: ")
    train = input("Train name: ")
    payment = int(input("Payment amount: "))
    departure = input("Date of departure (YYYY-MM-DD): ")
    phone = int(input("Phone number: "))
    aadhar = int(input("Aadhar number: "))

    sql = """INSERT INTO customer (name_, name_of_train, payment, date_of_departure, phone_no, aadhar_no) 
             VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql, (name, train, payment, departure, phone, aadhar))
        conn.commit()
        print("Customer added successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
        options()

# === Display Trains ===
def display_trains():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM train")
    rows = cursor.fetchall()
    print("\n--- Trains ---")
    for row in rows:
        print(f"Arrival: {row[0]}, Name: {row[1]}, Cost: {row[2]}, Distance: {row[3]}")
        print(f"From: {row[4]} ➡️ To: {row[5]}")
        print(f"Current Location: {row[6]}")
        print("-----")
    cursor.close()
    conn.close()
    options()

# === Display Customers ===
def display_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    print("\n--- Customers ---")
    for row in rows:
        print(f"Name: {row[0]}, Train: {row[1]}, Payment: {row[2]}, Departure: {row[3]}, Phone: {row[4]}, Aadhar: {row[5]}")
    cursor.close()
    conn.close()
    options()

# === Display Bills ===
def display_bills():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills")
    rows = cursor.fetchall()
    print("\n--- Bills ---")
    for row in rows:
        print(f"Train Booked: {row[0]}, Cost: {row[1]}, Arrival: {row[2]}")
    cursor.close()
    conn.close()
    options()

# === Get Live Train Location ===
def get_live_location():
    train_number = input("Enter Train Number (e.g., 12306): ")
    date = input("Enter Journey Date (DD-MM-YYYY): ")
    url = f"https://api.railwayapi.com/v2/live/train/{train_number}/date/{date}/apikey/{API_KEY}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Live Status:", data.get('position'))
        else:
            print("Failed to get data:", response.status_code)
    except Exception as e:
        print("API Error:", e)
    options()

# === Check Seat Availability ===
def check_seat_availability():
    train_number = input("Enter Train Number (e.g., 12306): ")
    source = input("Source Station Code (e.g., NDLS): ")
    destination = input("Destination Station Code (e.g., BCT): ")
    date = input("Journey Date (DD-MM-YYYY): ")
    class_code = input("Class Code (e.g., SL, 3A, 2A): ")
    quota = input("Quota Code (e.g., GN): ")

    url = f"https://api.railwayapi.com/v2/check-seat/train/{train_number}/source/{source}/dest/{destination}/date/{date}/pref/{class_code}/quota/{quota}/apikey/{API_KEY}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n--- Seat Availability ---")
            for avail in data.get('availability', []):
                print(f"Date: {avail['date']} | Status: {avail['status']}")
        else:
            print("Failed to fetch seat data.")
    except Exception as e:
        print("Error:", e)
    options()

# === Run App ===
signin()


