import oracledb


def get_connection():
    return oracledb.connect(
        user="shivani",          
        password="shivani",      
        dsn="localhost:1521/XEPDB1"
    )


class EmployeeManagementSystem:


    def add_employee(self):
        conn = get_connection()
        cur = conn.cursor()

        try:
            emp_id = input("Enter ID: ").strip()
            name = input("Enter Name: ").strip()
            age = int(input("Enter Age: "))

    
            if age <= 0:
                print("❌ Age must be greater than 0")
                return

            dept = input("Enter Department: ").strip()
            salary = float(input("Enter Salary: "))

            cur.execute("""
                INSERT INTO employees (emp_id, name, age, department, salary)
                VALUES (:1, :2, :3, :4, :5)
            """, (emp_id, name, age, dept, salary))

            conn.commit()
            print("✅ Employee added successfully!")

        except Exception as e:
            print("❌ Error:", e)

        finally:
            cur.close()
            conn.close()

    def view_employees(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()

        print("\nID | Name | Age | Department | Salary")
        print("--------------------------------------")

        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found")

        cur.close()
        conn.close()

    
    def search_employee(self):
        conn = get_connection()
        cur = conn.cursor()

        emp_id = input("Enter ID to search: ").strip()

        cur.execute("SELECT * FROM employees WHERE emp_id = :1", (emp_id,))
        row = cur.fetchone()

        if row:
            print("✅ Employee Found:")
            print(row)
        else:
            print("❌ Employee not found")

        cur.close()
        conn.close()

    
    def update_employee(self):
        conn = get_connection()
        cur = conn.cursor()

        emp_id = input("Enter Employee ID: ").strip()

        print("\n1. Update Name")
        print("2. Update Age")
        print("3. Update Department")
        print("4. Update Salary")

        choice = input("Enter choice: ")

        try:
            if choice == '1':
                new_value = input("Enter new name: ").strip()
                cur.execute("UPDATE employees SET name=:1 WHERE emp_id=:2", (new_value, emp_id))

            elif choice == '2':
                new_value = int(input("Enter new age: "))
                
                # 🔥 AGE VALIDATION
                if new_value <= 0:
                    print("❌ Age must be greater than 0")
                    return

                cur.execute("UPDATE employees SET age=:1 WHERE emp_id=:2", (new_value, emp_id))

            elif choice == '3':
                new_value = input("Enter new department: ").strip()
                cur.execute("UPDATE employees SET department=:1 WHERE emp_id=:2", (new_value, emp_id))

            elif choice == '4':
                new_value = float(input("Enter new salary: "))
                cur.execute("UPDATE employees SET salary=:1 WHERE emp_id=:2", (new_value, emp_id))

            else:
                print("❌ Invalid choice")
                return

            conn.commit()

            if cur.rowcount > 0:
                print("✅ Updated successfully!")
            else:
                print("❌ Employee not found")

        except Exception as e:
            print("❌ Error:", e)

        finally:
            cur.close()
            conn.close()

    # ---------------- DELETE EMPLOYEE ----------------
    def delete_employee(self):
        conn = get_connection()
        cur = conn.cursor()

        emp_id = input("Enter ID to delete: ").strip()

        cur.execute("DELETE FROM employees WHERE emp_id=:1", (emp_id,))
        conn.commit()

        if cur.rowcount > 0:
            print("✅ Employee deleted successfully!")
        else:
            print("❌ Employee not found")

        cur.close()
        conn.close()

    # ---------------- COUNT BY DEPARTMENT ----------------
    def count_by_department(self):
        conn = get_connection()
        cur = conn.cursor()

        dept = input("Enter Department: ").strip()

        cur.execute("SELECT COUNT(*) FROM employees WHERE department = :1", (dept,))
        count = cur.fetchone()[0]

        print(f"👥 Total employees in {dept}: {count}")

        cur.close()
        conn.close()


# ================== MAIN PROGRAM ==================
ems = EmployeeManagementSystem()

while True:
    print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Count Employees by Department")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        ems.add_employee()
    elif choice == '2':
        ems.view_employees()
    elif choice == '3':
        ems.search_employee()
    elif choice == '4':
        ems.update_employee()
    elif choice == '5':
        ems.delete_employee()
    elif choice == '6':
        ems.count_by_department()
    elif choice == '7':
        print("Exiting program...")
        break
    else:
        print("Invalid choice!")