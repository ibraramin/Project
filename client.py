import requests
import time
from classes import BloodGroup, Religion, Level, Department
from helper import print_enum_choice, printChoice, prettyPrint, coloredPrint

URL = "http://127.0.0.1:8000"


def collect_base_class_info():
    print("\n--- Personal Details ---")
    name = input("Name: ")
    pwd = input("Password: ")
    addr = input("Address: ")
    email = input("Email: ")
    bg = print_enum_choice(BloodGroup, "Blood Group")
    rel = print_enum_choice(Religion, "Religion")
    return {
        "name": name,
        "password": pwd,
        "address": addr,
        "email": email,
        "blood_group": bg,
        "religion": rel,
    }


def register():
    print("\n--- Register ---")
    print("1. Student")
    print("2. Faculty")
    type_choice = input("Select type: ")

    data = collect_base_class_info()
    endpoint = ""

    if type_choice == "1":
        endpoint = "/register/student"
        data["semester"] = int(input("Semester (1-8): ") or 1)
        data["dept"] = print_enum_choice(Department, "Department")
    elif type_choice == "2":
        endpoint = "/register/faculty"
        data["salary"] = int(input("Salary: ") or 0)
        data["level"] = print_enum_choice(Level, "Level")
        data["dept"] = print_enum_choice(Department, "Department")
    else:
        print("Invalid user type selection.")
        return

    try:
        response = requests.post(f"{URL}{endpoint}", json=data)
        if response.status_code == 200:
            user = response.json()
            coloredPrint(f"\nSuccess! Your User ID is: {user['id']}", "green")
            print("Please remember this ID to login.")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        coloredPrint("Cannot connect to server. Is main.py running?", "red")


def edit_user(user_data):
    prettyPrint("Edit Mode")
    print(f"Editing: {user_data['name']} ({user_data['type']})")

    new_data = {}

    name = input(f"Name [{user_data['name']}]: ")
    if name:
        new_data["name"] = name

    addr = input(f"Address [{user_data['address']}]: ")
    if addr:
        new_data["address"] = addr

    email = input(f"Email [{user_data.get('email', '')}]: ")
    if email:
        new_data["email"] = email

    if user_data["type"] == "faculty":
        sal = input(f"Salary [{user_data.get('salary', 0)}]: ")
        if sal:
            new_data["salary"] = int(sal)

    if user_data["type"] == "student":
        gpa = input(f"GPA [{user_data.get('gpa', 0.0)}]: ")
        if gpa:
            new_data["gpa"] = float(gpa)

    if not new_data:
        print("No changes made.")
        return

    try:
        res = requests.put(f"{URL}/update/user/{user_data['id']}", json=new_data)
        if res.status_code == 200:
            coloredPrint("Update Successful!", "green")
            
            return res.json().get("data")
        else:
            print("Update failed:", res.text)
    except Exception as e:
        print("Error:", e)
    return user_data


def login():
    print("\n--- Login ---")
    try:
        uid_input = input("User ID: ")
        if not uid_input.isdigit():
            print("ID must be a number.")
            return
        uid = int(uid_input)
        pwd = input("Password: ")
    except ValueError:
        print("Invalid input.")
        return

    try:
        res = requests.post(f"{URL}/login", json={"id": uid, "password": pwd})
        if res.status_code == 200:
            data = res.json()
            user = data["user"]
            coloredPrint(data["message"], "green")

            while True:
                print(f"\n--- User Menu ({user['type'].upper()}) ---")
                act = printChoice(["View Info", "Edit Info", "Logout"])

                if act == "1":
                    print("\n--- Your Data ---")
                    for k, v in user.items():
                        if (
                            k not in ["current_courses", "past_courses"]
                            and v is not None
                        ):
                            print(f"{k.replace('_', ' ').title()}: {v}")
                elif act == "2":
                    updated_user = edit_user(user)
                    if updated_user:
                        user = updated_user
                elif act == "3":
                    break
        else:
            coloredPrint("Login Failed: Wrong ID or Password", "red")
    except requests.exceptions.ConnectionError:
        print("Connection failed. Make sure the server is running.")


if __name__ == "__main__":
    prettyPrint("Uni System")
    while True:
        print("\n--- Main Menu ---")
        op = printChoice(["Login", "Register", "Quit"])

        if op == "1":
            login()
        elif op == "2":
            register()
        elif op == "3":
            print("Goodbye!")
            break
