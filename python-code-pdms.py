import mysql.connector
mycon = mysql.connector.connect(host="localhost", user="root", passwd="root", database="police")
cursor = mycon.cursor()
# Code for creating tables
def create_tables():
    sql1 = "create table officers(id int primary key auto_increment,Officer_Name varchar(50),DOB date,Age int(10),Marital_Status char(20),Officer_rank char(10),Salary int,Service_Duration varchar(50),Assigned_Station varchar(50),status char(50) default 'active')"
    cursor.execute(sql1)
    mycon.commit()
    sql1 = "create table duty(duty_id int primary key auto_increment,id int,duty char(50),duty_date date ,shift_start time ,shift_end time,duty_location VARCHAR(100))"
    cursor.execute(sql1)
    mycon.commit()
    sql1 = "create table Criminal_Records(Criminal_ID INT PRIMARY KEY AUTO_INCREMENT,Name varchar(50),Gender ENUM('male','female','other'),Age int(10),Address varchar(50),DOB date,Crimes_charged varchar(50),Arrest_Date date,Arresting_Officer char(50),Criminal_status enum('in custody','in parole','escaped','released'),case_status char(50) default 'active')"
    cursor.execute(sql1)
    mycon.commit()
    sql1 = "create table stolen_vehicle(Stolen_ID INT PRIMARY KEY AUTO_INCREMENT,License_Plate varchar(50),Vehicle_Type char(50),Vehicle_Make varchar(50),Vehicle_Color CHAR(20),Owner_Name VARCHAR(50),Location_Reported varchar(50),Time_Reported time,Date_Reported date,case_status char(50) default 'active')"
    cursor.execute(sql1)
    mycon.commit()
    sql1 = "create table man_missing(Missing_ID int primary key auto_increment,Name varchar(50),Father varchar(50),Mother varchar(50),Age int,gender varchar(50),Place varchar(50),Time time,Date date,status char(50) default 'active')"
    cursor.execute(sql1)
    mycon.commit()
    sql1 = 'create table police_login(id int primary key auto_increment,username char(50),password char(50))'
    cursor.execute(sql1)
    mycon.commit()
    sql1='create table admin_login(username varchar(100),password varchar(60))'
    cursor.execute(sql1)
    mycon.commit()

def register_officer():
    while True:
        username = input('Enter a username (min 5 characters): ')
        password = input('Enter a password (min 8 characters): ')
        if len(username) < 5:
            print("Username must be at least 5 characters long.")
            continue
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            continue
        confirm_password = input('Confirm your password: ')# Confirm the password
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue
        sql1 = 'SELECT * FROM police_login WHERE username = "{}"'.format(username)
        cursor.execute(sql1)
        if cursor.fetchone():
            print("Username already exists. Please choose a different username.")
            continue
        sql = 'INSERT INTO police_login (username,password) VALUES ( "{}", "{}")'.format(username,password)
        cursor.execute(sql)
        mycon.commit()
        print('Officer registered successfully.')
        sql1= 'select id from police_login where username="{}"'.format(username)
        cursor.execute(sql1)
        for i in cursor:
            print(' your officer id is',i[0])
        break  # Exit the loop once registration is successful

def login_officer():
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        sql='SELECT * FROM police_login WHERE username = "{}" AND password = "{}"'.format(username,password)
        cursor.execute(sql)
        if cursor.fetchone():
            print("Login successful. Welcome!",username)
            police_menu()
            break
        else:
            attempts -= 1
            if attempts > 0:
                print("Invalid credentials. Invalid credentials. You have",attempts," remaining.")
            else:
                print("Login failed. No attempts left.")

def admin_register():
    # Hypothesis for the admin password:
    # 1. Minimum length of 10 characters
    # 2. Contains at least one uppercase letter
    # 3. Includes at least one special character (e.g., '@' or '#')
    # 4. Contains a specific code or sequence ("101" or "ADM")
    while True:
        username = input("Enter new admin username: ")
        # Check if username already exists
        sql='SELECT * FROM admin_login WHERE username = "{}"'.format(username)
        cursor.execute(sql)
        if cursor.fetchone():
            print("Username already exists. Please choose a different username.")
            continue
        password = input("Enter new admin password: ")
        valid_password = True
        # Perform password validation checks
        if len(password) < 6:
            valid_password = False
        if not any(char.isupper() for char in password):
            valid_password = False
        if not any(char in "@#" for char in password):  # Special character rule
            valid_password = False
        if "PES$$" not in password and "02082007" not in password:  # Specific sequence known only to admin
            print("Password must contain a specific code or sequence known to the admin.")
            valid_password = False
        if valid_password is False:
            print("--------------------------------------------------------------\nThe password you entered doesn't meet the security requirements.\n--------------------------------------------------------------")
            continue  # start of the loop if the password is invalid
        confirm_password = input("Confirm your password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue  # Go back to the start of the loop if passwords do not match
        sql = 'INSERT INTO admin_login (username, password) VALUES ("{}", "{}")'.format(username, password)
        cursor.execute(sql)
        mycon.commit()
        print("Admin registered successfully.")
        break  # Exit the loop once registration is successful

def admin_login():
    attempts = 2  # Allow the user 2 attempts to log in
    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # Check if the username exists in the database
        cursor.execute('SELECT * FROM admin_login WHERE username = "{}" AND password = "{}"'.format(username, password))
        if cursor.fetchone():  
            print("Login successful! Welcome, admin.")
            admin_menu()
            break
        else:
            attempts = attempts-1
            if attempts > 0:
                print("Invalid credentials. You have",attempts," remaining.")
            else:
                print("Login failed. No attempts left.")
#**********************************************************************************************************************
#add officer admin only
def add_officer():
    name = input('Enter name of the officer')
    dob=input("Enter date of birth")
    age = int(input('enter officer age'))
    mar = input('officer married/Not married')
    rank = input('officer rank')
    sal = input('enter officer salary')
    ser = input('Enter officer service duration')
    ps = input('officer under which police station')
    sql1 = 'insert into officers(Officer_Name ,DOB,Age,Marital_status,Officer_rank,salary,Service_duration,Assigned_Station) values ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(name, dob, age, mar, rank, sal, ser, ps)
    cursor.execute(sql1)
    mycon.commit()

def search_officers():
    print("\n--- Officer Search Menu ---")
    print("1. Search by NAME\n2. Search by ID\n3. Search by RANK\n4. Search by STATION\n5. Search by DOB\n6. BACK")

    ch = input("Enter your choice: ")
    if ch == '1':
        value = input("Enter officer name: ")
        sql = "select * from officers where Officer_Name like '%{}%' and status='active'".format(value)
    elif ch == '2':
        value = int(input("Enter officer ID: "))
        sql = "select * from officers where id={} and status='active'".format(value)
    elif ch == '3':
        value = input("Enter officer rank: ")
        sql = "select * from officers where Officer_rank='{}' and status='active'".format(value)
    elif ch == '4':
        value = input("Enter assigned station: ")
        sql = "select * from officers where Assigned_Station like '%{}%' and status='active'".format(value)
    elif ch == '5':
        value = input("Enter DOB (yy-mm-dd): ")
        sql = "select * from officers where DOB like '%{}%' and status='active'".format(value)
    elif ch == '6':
        return
    else:
        print("ERRORRRR!!!!!!!!!!!!!!!!!!!!")
        return
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        for i in results:
            print('*'*40)
            print("\nID:", i[0])
            print("Officer Name:", i[1])
            print("DOB:", i[2])
            print("Age:", i[3])
            print("Marital Status:", i[4])
            print("Officer Rank:", i[5])
            print("Salary:", i[6])
            print("Service Duration:", i[7])
            print("Assigned Station:", i[8])
            print("*" * 40)
    else:
        print("Invalid: No matching records found.")

def view_officer():
    sql='select * from officers where status="active"'
    cursor.execute(sql)
    result=cursor.fetchall()
    for i in result:
        print("ID:", i[0])
        print("Officer Name:",i[1])
        print("DOB:", i[2])
        print("Age:", i[3])
        print("Marital Status:",i[4])
        print("Officer Rank:",i[5])
        print("Salary:", i[6])
        print("Service Duration:",i[7])
        print("Assigned Station:",i[8])
        print("-"*30)
      
def update_officers():
    print('1.Name\n2.Age\n3.Marital_status\n4.Officer_rank\n5.salary\n6.Service_duration\n7.Police_Station')
    choice = input('what you want to update ')

    if choice == "1":
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result= cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0], "Name", result[1], "DOB", result[2], "Age", result[3], "Marital_Status", result[4], "Rank", result[5],"Salary", result[6], "Service_Duration", result[7], "PoliceSation", result[8])
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update? (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    nam = input("Enter new name to update: ")
                    sql1 = "update officers set Officer_Name ='{}' WHERE id = '{}'".format(nam,Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("Officer name has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('Do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        continue
                        print("Restarting the process...")
                    else:
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break

    elif choice == '2':
        while True:
            Id = input("Enter officer ID: ")

            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result= cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0])
                print("Name", result[1])
                print("DOB", result[2])
                print("Age", result[3])
                print("Marital_Status", result[4])
                print("Rank", result[5])
                print("Salary", result[6])
                print("Service_Duration", result[7])
                print("PoliceSation", result[8])
                print("-"*30)
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update?  (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    Age = input("Enter new age to update: ")
                    sql1= "UPDATE officers SET Age = '{}' WHERE id = '{}'".format(Age,Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("Officer age has been updated successfully.")
                    break
                elif confirm == "0":
                    ch=print('do you want to continue press y for yes/n for no')
                    if ch=='y':
                        continue
                        print("Restarting the process...")
                    else:
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break

    elif choice == '3':
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id ='{}'".format(Id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0], "Name", result[1], "DOB", result[2], "Age", result[3], "Marital_Status", result[4], "Rank", result[5],"Salary", result[6], "Service_Duration", result[7], "PoliceSation", result[8])
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update? (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    mar = input("Enter new marital status to update: ")
                    sql1 = "UPDATE officers SET Marital_Status = '{}' WHERE id = '{}'".format(mar,Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("Officer marital status has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        continue
                        print("Restarting the process...")
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1 for yes' or '0 for no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break

    elif choice == '4':
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0])
                print("Name", result[1])
                print("DOB", result[2])
                print("Age", result[3])
                print("Marital_Status", result[4])
                print("Rank", result[5])
                print("Salary", result[6])
                print("Service_Duration", result[7])
                print("PoliceSation", result[8])
                print("-"*30)
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update?  (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    ofrank = input("Enter new rank to update: ")
                    sql1 = "UPDATE officers SET Officer_rank = '{}' WHERE id = '{}'".format(ofrank,Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("Officer rank has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        continue
                        print("Restarting the process...")
                    else:
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break

    elif choice == '5':
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0], "Name", result[1], "DOB", result[2], "Age", result[3], "Marital_Status",result[4], "Rank", result[5],"Salary",result[6], "Service_Duration", result[7], "PoliceSation", result[8])
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update?  (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    sal= input("Enter new salary to update: ")
                    sql1 = "UPDATE officers SET salary = '{}' WHERE id = '{}'".format(sal, Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("salary has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        print("Restarting the process...")
                        continue

                    else:
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break
    elif choice == '6':
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0], "Name", result[1], "DOB",result[2], "Age", result[3], "Marital_Status", result[4], "Rank", result[5],"Salary", result[6], "Service_Duration", result[7], "PoliceSation", result[8])
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update?  (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    ser= input("Enter service duration to update: ")
                    sql1 = "UPDATE officers SET Service_duration = '{}' WHERE id = '{}'".format(ser, Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("service duration has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        print("Restarting the process...")
                        continue

                    else:
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break
    elif choice == '7':
        while True:
            Id = input("Enter officer ID: ")
            # Fetch the officer's information by ID to display and confirm
            sql = "SELECT * FROM officers WHERE id = '{}'".format(Id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display the officer's information
                print("Id", result[0], "Name", result[1], "DOB", result[2], "Age", result[3], "Marital_Status", result[4], "Rank", result[5],"Salary", result[6], "Service_Duration", result[7], "PoliceSation", result[8])
                # Ask for confirmation
                confirm = input("\nIs this the correct officer you want to update?  (press 1 for yes/ 0 for no): ")

                if confirm == "1":
                    # Proceed with the update if the user confirms
                    ass = input("Enter station to update: ")
                    sql1 = "UPDATE officers SET Assigned_Station = '{}' WHERE id = '{}'".format(ass, Id)
                    cursor.execute(sql1)
                    mycon.commit()
                    print("service duration has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = print('do you want to continue press y for yes/n for no')
                    if ch == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("No officer found with the entered ID. Please try again.")
                break
    else:
        print('wrong choice')
#***********************************************************************************************************************     
#add duty
def add_duty():
    pid = int(input('Enter the officer ID: '))
    duty = input('Enter the assigned duty: ')
    date = input('Enter the date of the duty (YYYY-MM-DD): ')
    start = input('Enter the shift start time (HH:MM): ')
    ends = input('Enter the shift end time (HH:MM): ')
    Place = input('Enter the location of the duty: ')
    sql = 'insert into duty(id,duty,duty_date,shift_start,shift_end,duty_location) values(%s,%s,%s,%s,%s,%s)'
    values = (pid, duty,date,start,ends, Place)
    cursor.execute(sql,values)
    mycon.commit()
#*************************************************************************************************************
#view duty
def view_duty():
    id = input('Enter your Police ID to view assigned duties: ')
    sql='select * from duty where id="{}"'.format(id)
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        for i in result:
            print('duty_id', i[0])
            print('id', i[1])
            print('duty', i[2])
            print('duty_date', i[3])
            print('shift_start', i[4])
            print('shift_end', i[5])
            print('duty_location', i[6])
            print("-" * 114)
    else:
        print('no duty for this id')

def search_duty():
    print('Search Duty Records by:')
    print('1. Officer ID')
    print('2. Duty')
    print('3. Duty Date')
    print('4. Duty Location')
    choice = input('Enter your choice: ')
    if choice == '1':
        pid = input('Enter Officer ID to search: ')
        sql = 'SELECT * FROM duty WHERE id = "{}"'.format(pid)
    elif choice == '2':
        duty = input('Enter Duty to search: ')
        sql = 'SELECT * FROM duty WHERE duty LIKE "%{}%"'.format(duty)
    elif choice == '3':
        date = input('Enter Duty Date to search (yyyy-mm-dd): ')
        sql = 'SELECT * FROM duty WHERE duty_date LIKE "%{}%"'.format(date)
    elif choice == '4':
        location = input('Enter Duty Location to search: ')
        sql = 'SELECT * FROM duty WHERE duty_location LIKE "%{}%"'.format(location)
    else:
        print('Invalid choice, please try again.')
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i in result:
            print("*"*40)
            print("Duty ID:", i[0])
            print("Police ID:", i[1])
            print("Duty:", i[2])
            print("Duty Date:", i[3])
            print("Start Time:", i[4])
            print("End Time:", i[5])
            print("Location:", i[6])
            print("*" * 40)
    else:
        print("No records found matching the criteria.")
#****************************************************************************************************************            
# update duty
def update_duty():
    print('1. Police ID\n2. Duty\n3. Duty Date\n4. Duty Start Time\n5. Duty End Time\n6. Duty Location')
    choice = input('What do you want to update? ')
    if choice == '1':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4] )
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_police_id = input("Enter new police ID to update: ")
                    sql_update = "UPDATE duty SET id = '{}' WHERE duty_id = '{}'".format(new_police_id,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Police ID has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    elif choice == '2':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4])
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_duty = input("Enter new duty to update: ")
                    sql_update = "UPDATE duty SET duty = '{}' WHERE duty_id = '{}'".format(new_duty,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Duty has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    elif choice == '3':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4])
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_duty_date = input("Enter new duty date to update (YYYY-MM-DD): ")
                    sql_update = "UPDATE duty SET duty_date = '{}' WHERE duty_id = '{}'".format(new_duty_date,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Duty date has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    elif choice == '4':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4])
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_shift_start = input("Enter new shift start time (HH:MM): ")
                    sql_update = "UPDATE duty SET shift_start = '{}' WHERE duty_id = '{}'".format(new_shift_start,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Duty start time has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    elif choice == '5':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4])
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_shift_end = input("Enter new shift end time (HH:MM): ")
                    sql_update = "UPDATE duty SET shift_end = '{}' WHERE duty_id = '{}'".format(new_shift_end,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Duty end time has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    elif choice == '6':
        while True:
            duty_id = input("Enter duty ID: ")
            sql = "SELECT * FROM duty WHERE duty_id = '{}'".format(duty_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Duty ID:", result[0])
                print("Police ID:", result[1])
                print("Duty:", result[2])
                print("Duty Date:", result[3])
                print("Start Time:", result[4])
                print("End Time:", result[5])
                print("Location:", result[6])
                confirm = input("\nIs this the correct duty you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_duty_location = input("Enter new duty location to update: ")
                    sql_update = "UPDATE duty SET duty_location = '{}' WHERE duty_id = '{}'".format(new_duty_location,duty_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Duty location has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No duty found with the entered ID. Please try again.")
                break
    else:
        print("Invalid choice. Please select a valid option.")
#***********************************************************************************************************************
#add records
def add_records():
    name = input('Enter name of criminal')
    gender=input('gender')
    age = int(input('enter criminal age'))
    address = input('Enter criminal address')
    dob = input('Enter DOB')
    crime = input('Enter crime charged')
    date=input('date of case')
    off=input('case charged officer name')
    crst=input('enter criminal status \nin custody,in parole,escaped,released')
    sql1 = 'insert into criminal_records(Name,Gender,Age,Address,DOB,Crimes_charged,Arrest_Date,Arresting_Officer,Criminal_status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (name,gender, age,address,dob,crime,date,off,crst)
    cursor.execute(sql1, values)
    mycon.commit()

#view criminal record
def view_criminal_record():
    sql='select * from criminal_records where case_status="active"'
    cursor.execute(sql)
    result=cursor.fetchall()
    for i in result:
        print("*"* 20)
        print("Criminal ID:", i[0])
        print("Name:" ,i[1])
        print("Gender:", i[2])
        print("Age:" ,i[3])
        print("Address:" ,i[4])
        print("Date of Birth:" ,i[5])
        print("Crimes Charged:" ,i[6])
        print("Arrest Date:" ,i[7])
        print("Arresting Officer:",i[8])
        print("Criminal Status:",i[9])
        print("*" * 20)

def search_criminal():
    print('****** Criminal Record Search ******\n''1. Search by name\n2. Search by gender\n3. Search by age\n4. Search by address\n 5. Search by DOB\n6. Search by crime\n7. Search by date\n8. Search by arresting officer\n9.Search by criminal status')
    ch = input('Enter your choice: ')
    if ch == '1':
        nam = input('Enter name to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Name LIKE "%{}%" AND case_status="active"'.format(nam)
    elif ch == '2':
        gen = input('Enter gender to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Gender LIKE "%{}%" AND case_status="active"'.format(gen)
    elif ch == '3':
        age = input('Enter age to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Age="{}" AND case_status="active"'.format(age)
    elif ch == '4':
        add = input('Enter address to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Address LIKE "%{}%" AND case_status="active"'.format(add)
    elif ch == '5':
        dob = input('Enter DOB (yyyy-mm-dd) to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE DOB LIKE "%{}%" AND case_status="active"'.format(dob)
    elif ch == '6':
        cri = input('Enter crime to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Crimes_charged LIKE "%{}%" AND case_status="active"'.format(cri)
    elif ch == '7':
        date = input('Enter arrest date (yyyy-mm-dd) to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Arrest_Date LIKE "%{}%" AND case_status="active"'.format(date)
    elif ch == '8':
        off = input('Enter arresting officer name to search: ')
        sql = 'SELECT * FROM Criminal_Records WHERE Arresting_Officer LIKE "%{}%" AND case_status="active"'.format(off)
    elif ch == '9':
        crim = input('Enter criminal status to search (in custody, in parole, escaped, released): ')
        sql = 'SELECT * FROM Criminal_Records WHERE Criminal_status LIKE "%{}%" AND case_status="active"'.format(crim)
    else:
        print('Invalid/wrong choice')
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i in result:
            print("Criminal ID:", i[0])
            print("Name:", i[1])
            print("Gender:", i[2])
            print("Age:", i[3])
            print("Address:", i[4])
            print("DOB:", i[5])
            print("Crime Charged:", i[6])
            print("Arrest Date:", i[7])
            print("Arresting Officer:", i[8])
            print("Criminal Status:", i[9])
    else:
        print("No records found matching the criteria.")
#update crime records
def update_criminal_record():
    print('1. Name\n2. Gender\n3. Age\n4. Address\n5. DOB\n6. Crime Charged\n7. Arrest Date\n8. Arresting Officer\n9. Criminal Status')
    choice = input('What do you want to update? ')
    if choice == '1':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = %s"
            cursor.execute(sql, (criminal_id,))
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_name = input("Enter new name of criminal: ")
                    sql_update = "UPDATE criminal_records SET Name = '{}' WHERE Criminal_ID = {}".format(new_name,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Name has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '2':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_gender = input("Enter new gender: ")
                    sql_update = "UPDATE criminal_records SET Gender = '{}' WHERE Criminal_ID = {}".format(new_gender,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Gender has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '3':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_age = input("Enter new age of criminal: ")
                    sql_update = "UPDATE criminal_records SET Age = {} WHERE Criminal_ID = {}".format(new_age,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Age has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '4':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_address = input("Enter new address of criminal: ")
                    sql_update = "UPDATE criminal_records SET Address = '{}' WHERE Criminal_ID = {}".format(new_address,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Address has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '5':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_dob = input("Enter new DOB (YYYY-MM-DD): ")
                    sql_update = "UPDATE criminal_records SET DOB = '{}' WHERE Criminal_ID = {}".format(new_dob,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Date of Birth has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '6':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_crime_charged = input("Enter new crime charged: ")
                    sql_update = "UPDATE criminal_records SET Crime_charged = '{}' WHERE Criminal_ID = {}".format(new_crime_charged,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Crime charged has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '7':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_arrest_date = input("Enter new arrest date (YYYY-MM-DD): ")
                    sql_update = "UPDATE criminal_records SET Arrest_Date = '{}' WHERE Criminal_ID = {}".format(new_arrest_date,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Arrest Date has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '8':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_arresting_officer = input("Enter new arresting officer name: ")
                    sql_update = "UPDATE criminal_records SET Arrest_Officer = '{}' WHERE Criminal_ID = {}".format(new_arresting_officer,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("Arresting Officer has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    elif choice == '9':
        while True:
            criminal_id = input("Enter Criminal ID: ")
            sql = "SELECT * FROM criminal_records WHERE Criminal_ID = {}".format(criminal_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("Criminal ID:", result[0])
                print("Name:", result[1])
                print("Gender:", result[2])
                print("Age:", result[3])
                print("Address:", result[4])
                print("DOB:", result[5])
                print("Crime Charged:", result[6])
                print("Arrest Date:", result[7])
                print("Arresting Officer:", result[8])
                print("Criminal Status:", result[9])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    criminal_status = input("Enter criminal status: ")
                    sql_update = "UPDATE criminal_records SET Criminal Status = '{}' WHERE Criminal_ID = {}".format(criminal_status,criminal_id)
                    cursor.execute(sql_update)
                    mycon.commit()
                    print("status has been updated successfully.")
                    break
                elif confirm == "0":
                    ch = input('Do you want to continue? (y for yes / n for no): ')
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    else:
        print("Invalid choice. Please select a valid option.")
#******************************************************************************************************************************************       
#add stolen vehicle   
def add_auto_theft():
    License = input('Enter License number')
    Type = input('Enter vehicle type')
    Make = input('Enter Vehicle make')
    color = input('Enter color')
    owner = input('Enter Owner name')
    place = input('Enter place ')
    time = input('Enter crime time')
    date = input('Enter crime date')
    sql1= 'insert into stolen_vehicle(License_plate,Vehicle_Type,Vehicle_Make,Vehicle_Color,Owner_Name,Location_Reported,Time_Reported,Date_Reported) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (License,Type,Make,color,owner,place,time,date)
    cursor.execute(sql1, values)
    mycon.commit()
#update stolen vehcile
def view_stolen_vehicle():
    sql = 'select * from stolen_vehicle where case_status="active"'
    cursor.execute(sql)
    result =cursor.fetchall()
    if result:
        for i in result:
            print("Stolen ID:", i[0])
            print("License Plate:", i[1])
            print("Vehicle Type:", i[2])
            print("Vehicle Make:", i[3])
            print("Vehicle Color:", i[4])
            print("Owner Name:", i[5])
            print("Location Reported:", i[6])
            print("Time Reported:", i[7])
            print("Date Reported:", i[8])
            print("*" * 20)
    else:
        print('No records found')

def search_stolen_vehicle():
    print('Sort the record by\n1.License_plate\n2.Vehicle_Type\n3.Vehicle_Make\n4.Vehicle_Color\n5.Owner_Name\n6.Location_Reported\n7.Time_Reported\n8.Date_Reported')
    ch = input('Enter your choice: ')
    if ch == '1':
        lic = input('Enter license plate to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE License_Plate="{}" AND case_status="active"'.format(lic)
    elif ch == '2':
        veh = input('Enter vehicle type to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Vehicle_Type="{}" AND case_status="active"'.format(veh)
    elif ch == '3':
        veh = input('Enter vehicle make to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Vehicle_Make="{}" AND case_status="active"'.format(veh)
    elif ch == '4':
        veh = input('Enter vehicle color to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Vehicle_Color="{}" AND case_status="active"'.format(veh)
    elif ch == '5':
        own = input('Enter owner name to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Owner_Name LIKE "%{}%" AND case_status="active"'.format(own)
    elif ch == '6':
        loc = input('Enter location to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Location_Reported="{}" AND case_status="active"'.format(loc)
    elif ch == '7':
        time = input('Enter time to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Time_Reported="{}" AND case_status="active"'.format(time)
    elif ch == '8':
        date = input('Enter date to search: ')
        sql = 'SELECT * FROM stolen_vehicle WHERE Date_Reported="{}" AND case_status="active"'.format(date)
    else:
        print('Invalid choice')
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i in result:
            print("\nStolen ID:", i[0])
            print("License Plate:", i[1])
            print("Type:", i[2])
            print("Make:", i[3])
            print("Color:", i[4])
            print("Owner:", i[5])
            print("Location Reported:", i[6])
            print("Time Reported:", i[7])
            print("Date Reported:", i[8])
    else:
        print("No records found matching the criteria.")

def update_stolen_vehicle():
    print('1. License Plate\n2. Type\n3. Make\n4. Color\n5. Owner\n6. Place\n7. Time\n8. Date')
    choice = input('What do you want to update? ')
    if choice == '1':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_license_plate = input("Enter new license plate: ")
                    sql_update = "UPDATE stolen_vehicle SET License_Plate = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_license_plate, stolen_id))
                    mycon.commit()
                    print("License plate updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '2':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_vehicle_type = input("Enter new vehicle type: ")
                    sql_update = "UPDATE stolen_vehicle SET Vehicle_Type = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_vehicle_type, stolen_id))
                    mycon.commit()
                    print("Vehicle type updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '3':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_make = input("Enter new vehicle make: ")
                    sql_update = "UPDATE stolen_vehicle SET Vehicle_Make = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_make, stolen_id))
                    mycon.commit()
                    print("Vehicle make updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '4':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_color = input("Enter new vehicle color: ")
                    sql_update = "UPDATE stolen_vehicle SET Vehicle_Color = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_color, stolen_id))
                    mycon.commit()
                    print("Vehicle color updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '5':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_owner = input("Enter new owner name: ")
                    sql_update = "UPDATE stolen_vehicle SET Owner_Name = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_owner, stolen_id))
                    mycon.commit()
                    print("Owner name updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '6':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_place = input("Enter new place reported: ")
                    sql_update = "UPDATE stolen_vehicle SET Location_Reported = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_place, stolen_id))
                    mycon.commit()
                    print("Location reported updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
    elif choice == '7':
            while True:
                stolen_id = input("Enter Stolen ID: ")
                sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
                cursor.execute(sql, (stolen_id,))
                result = cursor.fetchone()
                if result:
                    print("\nStolen ID:", result[0])
                    print("License Plate:", result[1])
                    print("Type:", result[2])
                    print("Make:", result[3])
                    print("Color:", result[4])
                    print("Owner:", result[5])
                    print("Location Reported:", result[6])
                    print("Time Reported:", result[7])
                    print("Date Reported:", result[8])
                    confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                    if confirm == "1":
                        new_time = input("Enter new time reported (HH:MM): ")
                        sql_update = "UPDATE stolen_vehicle SET Time_Reported = %s WHERE Stolen_ID = %s"
                        cursor.execute(sql_update, (new_time, stolen_id))
                        mycon.commit()
                        print("Time reported updated successfully.")
                        break
                    elif confirm == "0":
                        ch = input("Do you want to continue? (y for yes / n for no): ")
                        if ch.lower() == 'y':
                            print("Restarting the process...")
                            continue
                        else:
                            break
                    else:
                        print("Invalid input. Please enter '1' for yes or '0' for no.")
                else:
                    print("No record found with the entered ID. Please try again.")
    elif choice == '8':
        while True:
            stolen_id = input("Enter Stolen ID: ")
            sql = "SELECT * FROM stolen_vehicle WHERE Stolen_ID = %s"
            cursor.execute(sql, (stolen_id,))
            result = cursor.fetchone()
            if result:
                print("\nStolen ID:", result[0])
                print("License Plate:", result[1])
                print("Type:", result[2])
                print("Make:", result[3])
                print("Color:", result[4])
                print("Owner:", result[5])
                print("Location Reported:", result[6])
                print("Time Reported:", result[7])
                print("Date Reported:", result[8])
                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")

                if confirm == "1":
                    new_date = input("Enter new date reported (YYYY-MM-DD): ")
                    sql_update = "UPDATE stolen_vehicle SET Date_Reported = %s WHERE Stolen_ID = %s"
                    cursor.execute(sql_update, (new_date, stolen_id))
                    mycon.commit()
                    print("Date reported updated successfully.")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No record found with the entered ID. Please try again.")
                break
    else:
        print("Invalid choice. Please select a valid option.")
#*********************************************************************************************************
#add_man_miss
def add_man_missing():
    name = input('Enter missing person name ')
    father=input('Enter Father name of missing person')
    mother=input('enter mother name of missing person')
    age = int(input('enter age of missing person'))
    gen=input('enter gender of missing person')
    place = input('Enter missing place')
    time = input('Enter time of missing')
    date = input('Enter date of missing')
    sql1 = 'insert into man_missing(Name,Father,Mother,Age,gender,Place,Time,Date) values ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(name,father,mother,age,gen,place,time,date)
    cursor.execute(sql1)
    mycon.commit()
    sql1='select * from man_missing where Name = "{}"'.format(name)
    cursor.execute(sql1)
    for i in cursor:
        print('CASE ID is', i[0])

def view_man_missing():
    sql='select * from man_missing where status="active"'
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        for i in result:
            print("Missing ID:",i[0],"\n""Name:",i[1],"\n""Father:",i[2],"\n""Mother:",i[3],"\n""Age:",i[4],"\n""Place:",i[5],"\n""Time:",i[6],"\n""Date:",i[7])
    else:
        print('No records found')

def search_man_missing():
    print('Sort the record by\n''1. By Missing person name\n2. Father name\n3. Mother name\n4. Age\n5. Missing-Place\n6. Missing-Time\n7. Missing-Date\n8. Gender')
    ch = input('Enter your choice: ')
    if ch == '1':
        nam = input('Enter name to search: ')
        sql = 'SELECT * FROM man_missing WHERE Name LIKE "%{}%" AND status="active"'.format(nam)
    elif ch == '2':
        nam = input('Enter father name to search: ')
        sql = 'SELECT * FROM man_missing WHERE Father LIKE "%{}%" AND status="active"'.format(nam)
    elif ch == '3':
        nam = input('Enter mother name to search: ')
        sql = 'SELECT * FROM man_missing WHERE Mother LIKE "%{}%" AND status="active"'.format(nam)
    elif ch == '4':
        age = input('Enter age to search: ')
        sql = 'SELECT * FROM man_missing WHERE Age="{}" AND status="active"'.format(age)
    elif ch == '5':
        pla = input('Enter place to search: ')
        sql = 'SELECT * FROM man_missing WHERE Place LIKE "%{}%" AND status="active"'.format(pla)
    elif ch == '6':
        time = input('Enter time to search: ')
        sql = 'SELECT * FROM man_missing WHERE Time LIKE "%{}%" AND status="active"'.format(time)
    elif ch == '7':
        date = input('Enter date to search (yyyy-mm-dd): ')
        sql = 'SELECT * FROM man_missing WHERE Date="{}" AND status="active"'.format(date)
    elif ch == '8':
        gen = input('Enter gender to search: ')
        sql = 'SELECT * FROM man_missing WHERE gender LIKE "%{}%" AND status="active"'.format(gen)
    else:
        print('Invalid/wrong choice')
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i in result:
            print("*" * 40)
            print("\nCurrent Record:")
            print("Missing ID:",i[0],"\n""Name:",i[1],"\n""Father:",i[2],"\n""Mother:",i[3],"\n""Age:",i[4],"\n""Place:",i[5],"\n""Time:",i[6],"\n""Date:",i[7])
            print("*" * 40)
    else:
        print("No records found matching the criteria.")

def update_missing_person():
    print('Update the record by\n1.by Missing person name\n2.Father name\n3.Mother name\n4.Age\n5.Missing-Place\n6.Missing-Time\n7.Missing-date')
    choice = input('What do you want to update? :')
    if choice == '1':
        while True:
            missing_id = input("Enter CASE ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:",result[0], "\n""Name:",result[1],"\n""Father:",result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_name = input("Enter new name: ")
                    query = "UPDATE man_missing SET Name = = '{}' WHERE Missing_ID = = '{}'".format(new_name,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Name updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '2':
        while True:
            missing_id = input("Enter CASE ID : ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:",result[0],"\n""Name:",result[1],"\n""Father:",result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_father = input("Enter father's name to update: ")
                    query = "UPDATE man_missing SET Father = '{}' WHERE Missing_ID = '{}'".format(new_father,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Father's name updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '3':
        while True:
            missing_id = input("Enter CASE ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:",result[0],"\n""Name:",result[1],"\n""Father:",result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_mother = input("Enter mother's name to update : ")
                    query = "UPDATE man_missing SET Mother = '{}' WHERE Missing_ID = '{}'".format(new_mother,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Mother's name updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '4':
        while True:
            missing_id = input("Enter CASE ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:",result[0],"\n""Name:",result[1],"\n""Father:",result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_age = int(input("Enter new age: "))
                    query = "UPDATE man_missing SET Age = '{}' WHERE Missing_ID = '{}'".format(new_age,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Age updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '5':
        while True:
            missing_id = input("Enter CASE ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:", result[0],"\n""Name:",result[1],"\n""Father:", result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_place = input("Enter new place: ")
                    query = "UPDATE man_missing SET Place = '{}' WHERE Missing_ID = '{}'".format(new_place,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Place updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '6':
        while True:
            missing_id = input("Enter CASE ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = '{}'".format(missing_id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                # Display current record
                print("*" * 40)
                print("\nCurrent Record:")
                print("Missing ID:",result[0],"\n""Name:",result[1],"\n""Father:",result[2],"\n""Mother:",result[3],"\n""Age:",result[4],"\n""Place:",result[5],"\n""Time:",result[6],"\n""Date:",result[7])
                print("*" * 40)

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_time = input("Enter new time: ")
                    query = "UPDATE man_missing SET Time = '{}' WHERE Missing_ID = '{}'".format(new_time,missing_id)
                    cursor.execute(query)
                    mycon.commit()
                    print("Time updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    elif choice == '7':
        while True:
            missing_id = input("Enter Missing Person ID: ")
            sql = "SELECT * FROM man_missing WHERE Missing_ID = %s"
            cursor.execute(sql, (missing_id,))
            result = cursor.fetchone()
            if result:
                # Display current record
                print("\nCurrent Record:")
                print("Missing ID:", result[0], "Name:", result[1], "Father:", result[2],
                      "Mother:", result[3], "Age:", result[4], "Place:", result[5],
                      "Time:", result[6], "Date:", result[7])

                confirm = input("\nIs this the correct record you want to update? (1 for yes / 0 for no): ")
                if confirm == "1":
                    new_date = input("Enter new date: ")
                    query = "UPDATE man_missing SET Date = %s WHERE Missing_ID = %s"
                    cursor.execute(query, (new_date, missing_id))
                    mycon.commit()
                    print("Date updated successfully.\n")
                    break
                elif confirm == "0":
                    ch = input("Do you want to continue? (y for yes / n for no): ")
                    if ch.lower() == 'y':
                        print("Restarting the process...\n")
                        continue
                    else:
                        break
                else:
                    print("Invalid input. Please enter '1' for yes or '0' for no.")
            else:
                print("No missing person found with the entered ID. Please try again.")
    else:
        print("Invalid choice. Please select a valid option.")
#*******************************************************************************************************
#for deleting and view deleted 
def delete_officers():
    oid = input("Enter ID to delete: ")
    # Display officer details before deleting
    sql1 = 'SELECT * FROM officers WHERE id=%s'
    cursor.execute(sql1, (oid,))
    i = cursor.fetchone()
    # Check if the officer ID exists
    if i:
        print("ID:", i[0])
        print("Officer Name:",i[1])
        print("DOB:", i[2])
        print("Age:", i[3])
        print("Marital Status:",i[4])
        print("Officer Rank:",i[5])
        print("Salary:", i[6])
        print("Service Duration:",i[7])
        print("Assigned Station:",i[8])
        print("-"*30)
        confirm = input("Are you sure you want to delete this officer? (1 for yes/0 for no): ")
        if confirm == "1":
            sql1= 'UPDATE officers SET status="inactive" WHERE id={}.'.format(oid)
            cursor.execute(sql1)
            mycon.commit()
            print("Officer has been deleted.")
        else:
            print("Operation canceled.")
    else:
        print("No officer found with the given ID.")

def delete_criminal_records():
    oid = input("Enter criminal ID to delete: ")
    # Display officer details before deleting
    sql1 = 'SELECT * FROM officers WHERE id="{}"'.format(oid)
    cursor.execute(sql1)
    i = cursor.fetchone()
    if i:# Check if the officer ID exists
        print("*"* 20)
        print("Criminal ID:", i[0])
        print("Name:" ,i[1])
        print("Gender:", i[2])
        print("Age:" ,i[3])
        print("Address:" ,i[4])
        print("Date of Birth:" ,i[5])
        print("Crimes Charged:" ,i[6])
        print("Arrest Date:" ,i[7])
        print("Arresting Officer:",i[8])
        print("Criminal Status:",i[9])
        print("*" * 20)
        confirm = input("Are you sure you want to delete this criminal ? (1 for yes/0 for no): ")
        if confirm == "1":
            sql1 = 'UPDATE Criminal_Records SET  case_status="inactive" WHERE Criminal_ID={}.'.format(oid)
            cursor.execute(sql1)
            mycon.commit()
            print("criminal has been deleted.")
        else:
            print("Operation canceled.")
    else:
        print("No criminal found with the given ID.")

def delete_stolen_vehicle():
    oid = input("Enter stolen ID to delete: ")
    # Display officer details before deleting
    sql1 = 'SELECT * FROM stolen_vehicle WHERE Stolen_ID="{}"'.format(oid)
    cursor.execute(sql1)
    i = cursor.fetchone()
    if i:# Check if the officer ID exists
        print("Stolen ID:", i[0])
        print("License Plate:", i[1])
        print("Vehicle Type:", i[2])
        print("Vehicle Make:", i[3])
        print("Vehicle Color:", i[4])
        print("Owner Name:", i[5])
        print("Location Reported:", i[6])
        print("Time Reported:", i[7])
        print("Date Reported:", i[8])
        print("*" * 20)
        confirm = input("Are you sure you want to delete this stolen vehicle? (1 for yes/0 for no): ")
        if confirm == "1":
            sql1 = 'UPDATE stolen_vehicle SET  case_status="inactive" WHERE Stolen_ID={}.'.format(oid)
            cursor.execute(sql1)
            mycon.commit()
            print("stolen case has been deleted.")
        else:
            print("Operation canceled.")
    else:
        print("No stolen case found with the given ID.")

def delete_man_missing():
    oid = input("Enter Case ID to delete: ")
    # Display officer details before deleting
    sql1 = 'SELECT * FROM man_missing WHERE Missing_ID="{}"'.format(oid)
    cursor.execute(sql1)
    i = cursor.fetchone()
    if i: # Check if the officer ID exists
        print("Missing ID:",i[0],"\n""Name:",i[1],"\n""Father:",i[2],"\n""Mother:",i[3],"\n""Age:",i[4],"\n""Place:",i[5],"\n""Time:",i[6],"\n""Date:",i[7])
        confirm = input("Are you sure you want to delete this man missing case? (1 for yes/0 for no): ")
        if confirm == "1":
            sql1 = 'UPDATE man_missing SET status="inactive" WHERE Missing_ID={}.'.format(oid)
            cursor.execute(sql1)
            mycon.commit()
            print("man missing case has been deleted.")
        else:
            print("Operation canceled.")
    else:
        print("No  found with the given ID.")

def view_delete():
    print("1.officer\n2.criminal\n3.stolen vehicle\n4.man missing\n5. GO BACK")
    ch=input('enter your choice')
    if ch=='1':
        sql='SELECT * FROM officers WHERE status="inactive"'
        cursor.execute(sql)
        for i in cursor:
            print("ID:", i[0])
            print("Officer Name:",i[1])
            print("DOB:", i[2])
            print("Age:", i[3])
            print("Marital Status:",i[4])
            print("Officer Rank:",i[5])
            print("Salary:", i[6])
            print("Service Duration:",i[7])
            print("Assigned Station:",i[8])
            print("-"*30)
    elif ch=='2':
        sql='SELECT * FROM Criminal_Records WHERE  status="inactive"'
        cursor.execute(sql)
        for i in cursor:
            print(i)
    elif ch=='3':
        sql='select * from stolen_vehicle where status="inactive"'
        cursor.execute(sql)
        for i in cursor:
            print(i)
    elif ch=='4':
        sql='select * from man_missing where status="inactive"'
        cursor.execute(sql)
        for i in cursor:
            print(i)
    elif ch=='5':
        admin_menu()
    else:
        print('No Records Found')

def admin_menu():
    while True:
        print("Admin Menu")
        print("1. Manage Officers")
        print("2. Manage Duties")
        print("3. Manage Criminal Records")
        print("4. Manage Stolen Vehicle")
        print("5. Manage Man Missing")
        print("6. Close case and update status")
        print('7. view closed case and status')
        print('8. Exit admin menu')
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                print("Managing Officers - \n1 Add officer,\n2 Update Officer,\n3 Search officer\n4.view officers(all)\n5. Go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    add_officer()
                elif ch == 2:
                    update_officers()
                elif ch == 3:
                    search_officers()
                elif ch == 4:
                    view_officer()
                elif ch==5:
                    admin_menu()
                else:
                    print('Wrong choice')
                print('do you want to continue officer menu y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '2':
            while True:
                print("Managing Duties...")
                print("Managing Officers - \n1 Add duty\n2 Update Duty\n3 view duty\n4.search duty\n5.Go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    add_duty()
                elif ch == 2:
                    update_duty()
                elif ch == 3:
                    view_duty()
                elif ch==4:
                    search_duty()
                elif ch==5:
                    admin_menu()
                else:
                    print('Wrong choice')
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '3':
            while True:
                print("Managing Criminal Records...")
                print("Managing Officers - \n1 Add record\n2 Update record\n3 Search criminal\n4 view criminal\n5.Go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    add_records()
                elif ch == 2:
                    update_criminal_record()
                elif ch == 3:
                    search_criminal()
                elif ch == 4:
                    view_criminal_record()
                elif ch ==5:
                    admin_menu()
                else:
                    print('Wrong choice')
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '4':
            while True:
                print("Managing Stolen Vehicle")
                print("Managing Stolen Vehicle - \n1 Add vehicle\n2 View Vehicle\n3 Search vehicle\n4 Update Vehicle\n5. Go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    add_auto_theft()
                elif ch == 2:
                    view_stolen_vehicle()
                elif ch == 3:
                    search_stolen_vehicle()
                elif ch == 4:
                    update_stolen_vehicle()
                elif ch ==5:
                    admin_menu()
                else:
                    print('Wrong choice')
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch.lower()== 'y':
                    continue
                else:
                    break
        elif choice == '5':
            while True:
                print("Manage Man Missing ")
                print("Managing Man Missing - \n1.Add man missing details\n2.View details\n3.Search Man missing\n4.Update Details\n5.Go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    add_man_missing()
                elif ch == 2:
                    view_man_missing()
                elif ch == 3:
                    search_man_missing()
                elif ch == 4:
                    update_missing_person()
                elif ch == 5:
                    admin_menu()
                else:
                    print('Wrong choice')
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice=='6':
            while True:
                print('1.for marking officers not in service')
                print('2.close man missing case')
                print('3.close stolen vehicle case')
                print('4.marking criminal status(no active cases)')
                print('5. Go back')
                ch = input('enter your choice')
                if ch == '1':
                    delete_officers()
                elif ch == '2':
                    delete_man_missing()
                elif ch == '3':
                    stolen_vehicle()
                elif ch == '4':
                    delete_criminal_records()
                elif ch =='5':
                    admin_menu()
                else:
                    print('invalid choice')
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch == 'y':
                    continue
                else:
                    break
        elif choice == '7':
            while True:
                view_delete()
                print('do you want to continue this menu y/n')
                ch = input('enter choice y/n')
                if ch == 'y':
                    continue
                else:
                    break
        elif choice=='8':
            char_menu()

def police_menu():
    while True:
        print("Police Menu")
        print("1. view/search Officers")
        print("2. view Duties")
        print("3. Manage Criminal Records")
        print("4. Manage Stolen Vehicle")
        print("5. Manage Man Missing")
        print('6. Go Back to log in/up')
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                print("Managing Officers - \n1. view officer,\n2. Search officer\n3.go back")
                ch = int(input('enter choice'))
                if ch == 1:
                    view_officer()
                elif ch == 2:
                    search_officers()
                elif ch==3:
                    police_menu()
                else:
                    print('Wrong choice')
                print('do you want to countinue this men y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '2':
            while True:
                print("Managing Duties...")
                print("Managing Officers - \n1. search duty\n2. view duty\n3.GO BACK")
                ch = int(input('enter choice'))
                if ch == 1:
                    view_duty()
                elif ch == 2:
                    search_duty()
                elif ch==3:
                    police_menu()
                else:
                    print('Wrong choice')
                print('do you want to countinue this men y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '3':
            while True:
                print("Managing Criminal Records...")
                print("Managing Officers - \n1. Search criminal\n2. view criminal\n3.GO BACK")
                ch = int(input('enter choice'))
                if ch == 1:
                    search_criminal()
                elif ch == 2:
                    view_criminal_record()
                elif ch==3:
                    police_menu()
                else:
                    print('Wrong choice')
                print('do you want to countinue this men y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '4':
            while True:
                print("Managing Stolen Vehicle")
                print("Managing Officers -\n1. Search vehicle\n2. View Vehicle\n3. GO BACK")
                ch = int(input('enter choice'))
                if ch == 1:
                    search_stolen_vehicle()
                elif ch == 2:
                    view_stolen_vehicle()
                elif ch==3:
                    police_menu()
                else:
                    print('Wrong choice')
                print('do you want to countinue this men y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice == '5':
            while True:
                print("Manage Man Missing ")
                print("Managing Officers - \n1. View details\n2. Search Man missing\n3.GO BACK")
                ch = int(input('enter choice'))
                if ch == 1:
                    view_man_missing()
                elif ch == 2:
                    search_man_missing()
                elif ch==3:
                    police_menu()
                else:
                    print('Wrong choice')
                print('do you want to countinue this men y/n')
                ch = input('enter choice y/n')
                if ch.lower() == 'y':
                    continue
                else:
                    break
        elif choice=='6':
            char_menu()
            
def char_menu():
    while True:
        print('1.register police')
        print('2.register admin')
        print('3.login police')
        print('4.login admin')
        print('5.exit')
        ch = input('enter your choice')
        if ch == '1':
            register_officer()
        elif ch == '2':
            admin_register()
        elif ch == '3':
            login_officer()
        elif ch == '4':
            admin_login()
        elif ch=='5':
            exit()
        else:
            print('wrong choice')
        print('do you want to continue y/n')
        ch = input('enter choice y/n')
        if ch.lower() == 'y':
            continue
        else:
            break

char_menu()



