import mysql.connector
import bcrypt
from datetime import datetime

# Establishing MySQL connection
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# Password hashing functions
def hash_pw(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())

def check_pw(hashed_pw, pw):
    return bcrypt.checkpw(pw.encode('utf-8'), hashed_pw)

# Registration function
def register():
    name = input("Enter Name: ")
    email = input("Enter Email ID: ")
    contact = input("Enter Contact No.: ")
    address = input("Enter Address: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    hire_date = input("Enter Hire Date (YYYY-MM-DD): ")
    pw = input("Enter Password: ")
    confirm_pw = input("Confirm Password: ")

    if pw != confirm_pw:
        print("Passwords do not match.")
        return

    hashed_pw = hash_pw(pw)

    try:
        # Insert into users table (no employee table insertion here)
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_pw))
        db.commit()

        print("Registration successful! You can now log in.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Login function
def login():
    email = input("Enter Email ID: ")
    pw = input("Enter Password: ")

    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result and check_pw(result[1].encode('utf-8'), pw):
        print("Login successful! ")
        return result[0]  # Returns user ID (Manager's ID)
    else:
        print("Login failed. Check your credentials.")
        return None

# Function to list all employees
def list_employees():
    cursor.execute("SELECT emp_id, name, position FROM employees")
    employees = cursor.fetchall()
    if employees:
        print("\nEmployees:")
        for emp in employees:
            print(f" Employee ID: {emp[0]}, Name: {emp[1]}, Position: {emp[2]}")
    else:
        print("No employees found.")

# CRUD: Create new employee
def create_employee(manager_id):
    name = input("Enter Employee Name: ")
    contact = input("Enter Employee Contact No.: ")
    address = input("Enter Employee Address: ")
    dob = input("Enter Employee Date of Birth (YYYY-MM-DD): ")
    hire_date = input("Enter Employee Hire Date (YYYY-MM-DD): ")
    position = input("Enter Employee Position: ")

    try:
        salary = float(input("Enter Employee Salary: "))
    except ValueError:
        print("Please enter a valid salary.")
        return

    try:
        experience = int(input("Enter Employee Experience in Years: "))
    except ValueError:
        print("Please enter a valid number of years for experience.")
        return

    try:
        cursor.execute(
            "INSERT INTO employees (user_id, name, contact_no, address, dob, hire_date, position, salary, experience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (manager_id, name, contact, address, dob, hire_date, position, salary, experience)
        )
        db.commit()
        print("Employee created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# CRUD: Read employee details
def read_employee():
    list_employees()
    emp_id = input("Enter Employee ID to Read: ")
    cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
    emp = cursor.fetchone()
    if emp:
        print(f"ID: {emp[0]}, Name: {emp[2]}, Contact: {emp[3]}, Address: {emp[4]}, DOB: {emp[5]}, Hire Date: {emp[6]}, Position: {emp[7]}, Salary: {emp[8]}, Experience: {emp[9]} years")
    else:
        print("Employee not found.")

# CRUD: Update employee details
def update_employee():
    list_employees()
    emp_id = input("Enter Employee ID to Update: ")
    new_contact = input("Enter new Contact No.: ")
    new_address = input("Enter new Address: ")
    cursor.execute("UPDATE employees SET contact_no = %s, address = %s WHERE emp_id = %s",
                   (new_contact, new_address, emp_id))
    db.commit()
    print("Employee details updated successfully.")

# CRUD: Delete employee
def delete_employee():
    list_employees()
    emp_id = input("Enter Employee ID to Delete: ")
    cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
    db.commit()
    print("Employee deleted successfully.")

# CRUD: Add performance review
def add_review():
    list_employees()
    emp_id = input("Enter Employee ID to Add Review: ")
    cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
    employee = cursor.fetchone()
    if not employee:
        print("No employee found with the given ID.")
        return
    rating = float(input("Enter Rating (1.0-5.0): "))
    feedback = input("Enter Feedback: ")
    review_date = datetime.now().date()

    cursor.execute(
        "INSERT INTO performance_reviews (employee_id, review_date, rating, feedback) VALUES (%s, %s, %s, %s)",
        (emp_id, review_date, rating, feedback))
    db.commit()
    print("Performance review added successfully.")

# CRUD: View performance reviews
def view_reviews():
    list_employees()
    emp_id = input("Enter Employee ID to View Reviews: ")
    cursor.execute("SELECT * FROM performance_reviews WHERE employee_id = %s", (emp_id,))
    reviews = cursor.fetchall()
    print("\nPerformance Reviews:")
    for review in reviews:
        print(f"Date: {review[2]}, Rating: {review[3]}, Feedback: {review[4]}")

# CRUD: Update performance review
def update_review():
    list_employees()
    review_id = input("Enter Review ID to Update: ")
    new_rating = float(input("Enter new Rating (1.0-5.0): "))
    new_feedback = input("Enter new Feedback: ")
    cursor.execute("UPDATE performance_reviews SET rating = %s, feedback = %s WHERE review_id = %s",
                   (new_rating, new_feedback, review_id))
    db.commit()
    print("Review updated successfully.")

# CRUD: Delete performance review
def delete_review():
    list_employees()
    review_id = input("Enter Review ID to Delete: ")
    cursor.execute("DELETE FROM performance_reviews WHERE review_id = %s", (review_id,))
    db.commit()
    print("Review deleted successfully.")

def promote_employee():
    list_employees()  # Show all employees
    emp_id = input("Enter Employee ID to Promote: ")

    cursor.execute("SELECT name, position, salary, experience FROM employees WHERE emp_id = %s", (emp_id,))
    employee = cursor.fetchone()

    if not employee:
        print("No employee found with the given ID.")
        return

    name, current_position, current_salary, experience = employee
    print(f"Current Position: {current_position}, Current Salary: ${current_salary}, Years of Experience: {experience}")

    positions = {
        1: ("DevOps Engineer", 60000),
        2: ("Build Engineer", 65000),
        3: ("Reliability Engineer", 70000),
        4: ("Release Manager", 80000),
        5: ("Data Analyst", 85000),
        6: ("Product Manager", 90000)
    }

    print("Available Positions for Promotion:")
    for num, (pos, sal) in positions.items():
        print(f"{num}. {pos} - ${sal}")

    # Get user input as a number
    while True:
        try:
            choice = int(input("Select new position by entering the number: "))
            if choice in positions:
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number.")

    new_position, new_salary = positions[choice]

    # Update the employee's position and salary
    cursor.execute("UPDATE employees SET position = %s, salary = %s WHERE emp_id = %s",
                   (new_position, new_salary, emp_id))
    db.commit()

    # Show the promotion details
    print(f"\nEmployee {name} promoted!")
    print(f"Previous Position: {current_position}, Previous Salary: ${current_salary}")
    print(f"New Position: {new_position}, New Salary: ${new_salary}")

def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                while True:
                    print("\n1. Create Employee")
                    print("2. Read Employee")
                    print("3. Update Employee")
                    print("4. Delete Employee")
                    print("5. Add Performance Review")
                    print("6. View Performance Reviews")
                    print("7. Update Performance Review")
                    print("8. Delete Performance Review")
                    print("9. Promote Employee")
                    print("10. Logout")
                    action = input("Enter your action: ")

                    if action == '1':
                        create_employee(user_id)
                    elif action == '2':
                        read_employee()
                    elif action == '3':
                        update_employee()
                    elif action == '4':
                        delete_employee()
                    elif action == '5':
                        add_review()
                    elif action == '6':
                        view_reviews()
                    elif action == '7':
                        update_review()
                    elif action == '8':
                        delete_review()
                    elif action == '9':
                        promote_employee()
                    elif action == '10':
                        break
                    else:
                        print("Invalid action. Please select again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()