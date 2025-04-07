# import mysql.connector
# import bcrypt
# from datetime import datetime

# # Establishing MySQL connection
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Loads from .env

# db = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )

# cursor = db.cursor()

# # Password hashing functions
# def hash_pw(pw):
#     return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())

# def check_pw(hashed_pw, pw):
#     return bcrypt.checkpw(pw.encode('utf-8'), hashed_pw)

# # Registration function
# def register():
#     name = input("Enter Name: ")
#     email = input("Enter Email ID: ")
#     contact = input("Enter Contact No.: ")
#     address = input("Enter Address: ")
#     dob = input("Enter Date of Birth (YYYY-MM-DD): ")
#     hire_date = input("Enter Hire Date (YYYY-MM-DD): ")
#     pw = input("Enter Password: ")
#     confirm_pw = input("Confirm Password: ")

#     if pw != confirm_pw:
#         print("Passwords do not match.")
#         return

#     hashed_pw = hash_pw(pw)

#     try:
#         # Insert into users table (no employee table insertion here)
#         cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_pw))
#         db.commit()

#         print("Registration successful! You can now log in.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

# # Login function
# def login():
#     email = input("Enter Email ID: ")
#     pw = input("Enter Password: ")

#     cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
#     result = cursor.fetchone()

#     if result and check_pw(result[1].encode('utf-8'), pw):
#         print("Login successful! ")
#         return result[0]  # Returns user ID (Manager's ID)
#     else:
#         print("Login failed. Check your credentials.")
#         return None

# # Function to list all employees
# def list_employees():
#     cursor.execute("SELECT emp_id, name, position FROM employees")
#     employees = cursor.fetchall()
#     if employees:
#         print("\nEmployees:")
#         for emp in employees:
#             print(f" Employee ID: {emp[0]}, Name: {emp[1]}, Position: {emp[2]}")
#     else:
#         print("No employees found.")

# # CRUD: Create new employee
# def create_employee(manager_id):
#     name = input("Enter Employee Name: ")
#     contact = input("Enter Employee Contact No.: ")
#     address = input("Enter Employee Address: ")
#     dob = input("Enter Employee Date of Birth (YYYY-MM-DD): ")
#     hire_date = input("Enter Employee Hire Date (YYYY-MM-DD): ")
#     position = input("Enter Employee Position: ")

#     try:
#         salary = float(input("Enter Employee Salary: "))
#     except ValueError:
#         print("Please enter a valid salary.")
#         return

#     try:
#         experience = int(input("Enter Employee Experience in Years: "))
#     except ValueError:
#         print("Please enter a valid number of years for experience.")
#         return

#     try:
#         cursor.execute(
#             "INSERT INTO employees (user_id, name, contact_no, address, dob, hire_date, position, salary, experience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#             (manager_id, name, contact, address, dob, hire_date, position, salary, experience)
#         )
#         db.commit()
#         print("Employee created successfully!")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")


# # CRUD: Read employee details
# def read_employee():
#     list_employees()
#     emp_id = input("Enter Employee ID to Read: ")
#     cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
#     emp = cursor.fetchone()
#     if emp:
#         print(f"ID: {emp[0]}, Name: {emp[2]}, Contact: {emp[3]}, Address: {emp[4]}, DOB: {emp[5]}, Hire Date: {emp[6]}, Position: {emp[7]}, Salary: {emp[8]}, Experience: {emp[9]} years")
#     else:
#         print("Employee not found.")

# # CRUD: Update employee details
# def update_employee():
#     list_employees()
#     emp_id = input("Enter Employee ID to Update: ")
#     new_contact = input("Enter new Contact No.: ")
#     new_address = input("Enter new Address: ")
#     cursor.execute("UPDATE employees SET contact_no = %s, address = %s WHERE emp_id = %s",
#                    (new_contact, new_address, emp_id))
#     db.commit()
#     print("Employee details updated successfully.")

# # CRUD: Delete employee
# def delete_employee():
#     list_employees()
#     emp_id = input("Enter Employee ID to Delete: ")
#     cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
#     db.commit()
#     print("Employee deleted successfully.")

# # CRUD: Add performance review
# def add_review():
#     list_employees()
#     emp_id = input("Enter Employee ID to Add Review: ")
#     cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
#     employee = cursor.fetchone()
#     if not employee:
#         print("No employee found with the given ID.")
#         return
#     rating = float(input("Enter Rating (1.0-5.0): "))
#     feedback = input("Enter Feedback: ")
#     review_date = datetime.now().date()

#     cursor.execute(
#         "INSERT INTO performance_reviews (employee_id, review_date, rating, feedback) VALUES (%s, %s, %s, %s)",
#         (emp_id, review_date, rating, feedback))
#     db.commit()
#     print("Performance review added successfully.")

# # CRUD: View performance reviews
# def view_reviews():
#     list_employees()
#     emp_id = input("Enter Employee ID to View Reviews: ")
#     cursor.execute("SELECT * FROM performance_reviews WHERE employee_id = %s", (emp_id,))
#     reviews = cursor.fetchall()
#     print("\nPerformance Reviews:")
#     for review in reviews:
#         print(f"Date: {review[2]}, Rating: {review[3]}, Feedback: {review[4]}")

# # CRUD: Update performance review
# def update_review():
#     list_employees()
#     review_id = input("Enter Review ID to Update: ")
#     new_rating = float(input("Enter new Rating (1.0-5.0): "))
#     new_feedback = input("Enter new Feedback: ")
#     cursor.execute("UPDATE performance_reviews SET rating = %s, feedback = %s WHERE review_id = %s",
#                    (new_rating, new_feedback, review_id))
#     db.commit()
#     print("Review updated successfully.")

# # CRUD: Delete performance review
# def delete_review():
#     list_employees()
#     review_id = input("Enter Review ID to Delete: ")
#     cursor.execute("DELETE FROM performance_reviews WHERE review_id = %s", (review_id,))
#     db.commit()
#     print("Review deleted successfully.")

# def promote_employee():
#     list_employees()  # Show all employees
#     emp_id = input("Enter Employee ID to Promote: ")

#     cursor.execute("SELECT name, position, salary, experience FROM employees WHERE emp_id = %s", (emp_id,))
#     employee = cursor.fetchone()

#     if not employee:
#         print("No employee found with the given ID.")
#         return

#     name, current_position, current_salary, experience = employee
#     print(f"Current Position: {current_position}, Current Salary: ${current_salary}, Years of Experience: {experience}")

#     positions = {
#         1: ("DevOps Engineer", 60000),
#         2: ("Build Engineer", 65000),
#         3: ("Reliability Engineer", 70000),
#         4: ("Release Manager", 80000),
#         5: ("Data Analyst", 85000),
#         6: ("Product Manager", 90000)
#     }

#     print("Available Positions for Promotion:")
#     for num, (pos, sal) in positions.items():
#         print(f"{num}. {pos} - ${sal}")

#     # Get user input as a number
#     while True:
#         try:
#             choice = int(input("Select new position by entering the number: "))
#             if choice in positions:
#                 break
#             else:
#                 print("Invalid choice. Please select a valid number.")
#         except ValueError:
#             print("Please enter a valid number.")

#     new_position, new_salary = positions[choice]

#     # Update the employee's position and salary
#     cursor.execute("UPDATE employees SET position = %s, salary = %s WHERE emp_id = %s",
#                    (new_position, new_salary, emp_id))
#     db.commit()

#     # Show the promotion details
#     print(f"\nEmployee {name} promoted!")
#     print(f"Previous Position: {current_position}, Previous Salary: ${current_salary}")
#     print(f"New Position: {new_position}, New Salary: ${new_salary}")

# def main():
#     while True:
#         print("\n1. Register")
#         print("2. Login")
#         print("3. Exit")
#         choice = input("Enter your choice: ")

#         if choice == '1':
#             register()
#         elif choice == '2':
#             user_id = login()
#             if user_id:
#                 while True:
#                     print("\n1. Create Employee")
#                     print("2. Read Employee")
#                     print("3. Update Employee")
#                     print("4. Delete Employee")
#                     print("5. Add Performance Review")
#                     print("6. View Performance Reviews")
#                     print("7. Update Performance Review")
#                     print("8. Delete Performance Review")
#                     print("9. Promote Employee")
#                     print("10. Logout")
#                     action = input("Enter your action: ")

#                     if action == '1':
#                         create_employee(user_id)
#                     elif action == '2':
#                         read_employee()
#                     elif action == '3':
#                         update_employee()
#                     elif action == '4':
#                         delete_employee()
#                     elif action == '5':
#                         add_review()
#                     elif action == '6':
#                         view_reviews()
#                     elif action == '7':
#                         update_review()
#                     elif action == '8':
#                         delete_review()
#                     elif action == '9':
#                         promote_employee()
#                     elif action == '10':
#                         break
#                     else:
#                         print("Invalid action. Please select again.")
#         elif choice == '3':
#             break
#         else:
#             print("Invalid choice. Please select again.")

# if __name__ == "__main__":
#     main()
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection
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
    return bcrypt.checkpw(pw.encode('utf-8'), hashed_pw.encode('utf-8'))

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.current_user = None
        
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack()
        
        ttk.Label(self.main_frame, text="Main Menu", font=('Arial', 16)).grid(row=0, column=0, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.show_register).grid(row=1, column=0, pady=5, sticky='ew')
        ttk.Button(self.main_frame, text="Login", command=self.show_login).grid(row=2, column=0, pady=5, sticky='ew')
        ttk.Button(self.main_frame, text="Exit", command=self.root.quit).grid(row=3, column=0, pady=5, sticky='ew')

    def show_register(self):
        RegisterWindow(self.root)
    
    def show_login(self):
        LoginWindow(self.root, self)

class RegisterWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Registration")
        
        self.create_widgets()
    
    def create_widgets(self):
        fields = [
            ("Name", "name"),
            ("Email ID", "email"),
            ("Contact No.", "contact"),
            ("Address", "address"),
            ("Date of Birth (YYYY-MM-DD)", "dob"),
            ("Hire Date (YYYY-MM-DD)", "hire_date"),
            ("Password", "password", True),
            ("Confirm Password", "confirm_password", True)
        ]
        
        self.entries = {}
        for i, (label, field, *is_password) in enumerate(fields):
            ttk.Label(self.top, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.top, show="*" if is_password else "")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        ttk.Button(self.top, text="Register", command=self.register).grid(row=len(fields), columnspan=2, pady=10)

    def register(self):
        data = {k: v.get() for k, v in self.entries.items()}
        
        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",
                          (data['email'], hash_pw(data['password'])))
            db.commit()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            self.top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Registration failed: {err}")

class LoginWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Login")
        
        ttk.Label(self.top, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(self.top)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.top, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.top, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.top, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        if result and check_pw(result[1], password):
            self.app.current_user = result[0]
            self.top.destroy()
            ManagerDashboard(self.app.root, self.app)
        else:
            messagebox.showerror("Error", "Invalid credentials")

class ManagerDashboard:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Manager Dashboard")
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self.top, text="Manager Dashboard", font=('Arial', 14)).pack(pady=10)
        
        buttons = [
            ("Employee Management", self.show_employee_management),
            ("Performance Reviews", self.show_performance_reviews),
            ("Promote Employee", self.promote_employee),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            ttk.Button(self.top, text=text, command=command).pack(fill='x', padx=20, pady=5)

    def show_employee_management(self):
        EmployeeManagementWindow(self.top, self.app)
    
    def show_performance_reviews(self):
        PerformanceReviewWindow(self.top, self.app)
    
    def promote_employee(self):
        PromoteWindow(self.top, self.app)
    
    def logout(self):
        self.top.destroy()
        self.app.current_user = None

class EmployeeManagementWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Employee Management")
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self.top, text="Employee Management", font=('Arial', 12)).pack(pady=10)
        
        buttons = [
            ("Create Employee", self.create_employee),
            ("View Employees", self.view_employees),
            ("Update Employee", self.update_employee),
            ("Delete Employee", self.delete_employee)
        ]
        
        for text, command in buttons:
            ttk.Button(self.top, text=text, command=command).pack(fill='x', padx=20, pady=5)

    def create_employee(self):
        CreateEmployeeWindow(self.top, self.app)
    
    def view_employees(self):
        ViewEmployeesWindow(self.top)
    
    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter Employee ID:")
        if emp_id:
            UpdateEmployeeWindow(self.top, emp_id)
    
    def delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter Employee ID:")
        if emp_id:
            try:
                cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
                db.commit()
                messagebox.showinfo("Success", "Employee deleted successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Delete failed: {err}")

class CreateEmployeeWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Create Employee")
        
        self.create_widgets()
    
    def create_widgets(self):
        fields = [
            ("Name", "name"),
            ("Contact No.", "contact"),
            ("Address", "address"),
            ("Date of Birth (YYYY-MM-DD)", "dob"),
            ("Hire Date (YYYY-MM-DD)", "hire_date"),
            ("Position", "position"),
            ("Salary", "salary"),
            ("Experience (years)", "experience")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(self.top, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.top)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        ttk.Button(self.top, text="Create", command=self.create).grid(row=len(fields), columnspan=2, pady=10)

    def create(self):
        data = {k: v.get() for k, v in self.entries.items()}
        try:
            cursor.execute(
                "INSERT INTO employees (user_id, name, contact_no, address, dob, hire_date, position, salary, experience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (self.app.current_user, data['name'], data['contact'], data['address'],
                 data['dob'], data['hire_date'], data['position'], data['salary'], data['experience'])
            )
            db.commit()
            messagebox.showinfo("Success", "Employee created successfully")
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Creation failed: {str(e)}")

class ViewEmployeesWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("View Employees")
        
        self.tree = ttk.Treeview(self.top, columns=('ID', 'Name', 'Position'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Position', text='Position')
        self.tree.pack(fill='both', expand=True)
        
        self.load_data()
    
    def load_data(self):
        cursor.execute("SELECT emp_id, name, position FROM employees")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

class PerformanceReviewWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Performance Reviews")
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self.top, text="Performance Reviews", font=('Arial', 12)).pack(pady=10)
        
        buttons = [
            ("Add Review", self.add_review),
            ("View Reviews", self.view_reviews),
            ("Update Review", self.update_review),
            ("Delete Review", self.delete_review)
        ]
        
        for text, command in buttons:
            ttk.Button(self.top, text=text, command=command).pack(fill='x', padx=20, pady=5)

    def add_review(self):
        AddReviewWindow(self.top, self.app)
    
    def view_reviews(self):
        ViewReviewsWindow(self.top)
    
    def update_review(self):
        review_id = simpledialog.askinteger("Input", "Enter Review ID:")
        if review_id:
            UpdateReviewWindow(self.top, review_id)
    
    def delete_review(self):
        review_id = simpledialog.askinteger("Input", "Enter Review ID:")
        if review_id:
            try:
                cursor.execute("DELETE FROM performance_reviews WHERE review_id = %s", (review_id,))
                db.commit()
                messagebox.showinfo("Success", "Review deleted successfully")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Delete failed: {err}")

class PromoteWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.app = app
        self.top.title("Promote Employee")
        
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self.top, text="Select Employee and New Position").pack(pady=10)
        
        # Employee selection
        ttk.Label(self.top, text="Employee ID:").pack()
        self.emp_id_entry = ttk.Entry(self.top)
        self.emp_id_entry.pack()
        
        # Position selection
        ttk.Label(self.top, text="New Position:").pack()
        self.position_var = tk.StringVar()
        positions = [
            "DevOps Engineer",
            "Build Engineer",
            "Reliability Engineer",
            "Release Manager",
            "Data Analyst",
            "Product Manager"
        ]
        self.position_menu = ttk.Combobox(self.top, textvariable=self.position_var, values=positions)
        self.position_menu.pack()
        
        ttk.Button(self.top, text="Promote", command=self.promote).pack(pady=10)

    def promote(self):
        emp_id = self.emp_id_entry.get()
        new_position = self.position_var.get()
        
        if not emp_id or not new_position:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return
        
        try:
            cursor.execute("UPDATE employees SET position = %s WHERE emp_id = %s",
                           (new_position, emp_id))
            db.commit()
            messagebox.showinfo("Success", "Employee promoted successfully")
            self.top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Promotion failed: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    db.close()