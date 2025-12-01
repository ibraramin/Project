import requests
from helper import *
from classes import BloodGroup, Religion, Level, Department

url = "http://127.0.0.1:8000"


def call_login():
    big_print("Login")
    id = int(input("User ID: "))
    password = input("Password: ")
    response = requests.post(f"{url}/login", json={"id": id, "password": password})
    if response.status_code == 200:
        user = response.json()["user"]
        colored_print(f"Welcome {user['name']}", "green")
        user_dashboard(user)
    else:
        colored_print("Login Failed", "red")


def call_register():
    big_print("Register")
    print("\n1. Student\n2. Faculty")
    choice = input("Select type: ")

    data = {
        "name": input("Name: "),
        "password": input("Password: "),
        "address": input("Address: "),
        "email": input("Email: "),
        "blood_group": select_enum(BloodGroup),
        "religion": select_enum(Religion),
    }

    if choice == "1":
        data["semester"] = int(input("Semester: ") or 1)
        data["dept"] = select_enum(Department)
        endpoint = "/register/student"
    elif choice == "2":
        data["salary"] = int(input("Salary: ") or 0)
        data["level"] = select_enum(Level)
        data["dept"] = select_enum(Department)
        endpoint = "/register/faculty"
    else:
        return

    response = requests.post(f"{url}{endpoint}", json=data)
    if response.status_code == 200:
        colored_print(f"Registered! ID: {response.json()['id']}", "green")
    else:
        print("Error:", response.text)


def user_dashboard(user):
    while True:
        big_print("Dashboard")
        print(f"\n{user['type']} Menu")

        if user["type"] == "student":
            ops = [
                "View Info",
                "Edit Info",
                "Add Course",
                "Drop Course",
                "Retake Course",
                "Logout",
            ]
        else:
            ops = ["View Info", "Edit Info", "Add Marks", "Logout"]

        sel = get_choice(ops)

        if sel == "1":
            big_print("User Info")
            for k, v in user.items():
                if v and k not in ["current_courses", "results"]:
                    print(f"{k}: {v}")
            if "current_courses" in user:
                print(f"Courses: {user['current_courses']}")
            if "results" in user:
                print(f"Results: {user['results']}")

        elif sel == "2":
            user = edit_user(user)

        elif sel == "3":
            if user["type"] == "student":
                enroll_course(user, retake_mode=False)
            else:
                upload_marks()

        elif sel == "4":
            if user["type"] == "student":
                drop_course(user)
            else:
                break

        elif sel == "5":
            if user["type"] == "student":
                enroll_course(user, retake_mode=True)
            else:
                pass

        elif user["type"] == "student" and sel == "6":
            break


def edit_user(user):
    updates = {}
    name = input(f"Name [{user['name']}]: ")
    if name:
        updates["name"] = name

    res = requests.put(f"{url}/user/{user['id']}", json=updates)
    if res.status_code == 200:
        colored_print("Updated!", "green")
        return res.json()["data"]
    return user


def enroll_course(user, retake_mode=False):
    res = requests.get(f"{url}/available_courses/{user['id']}")
    data = res.json()
    courses = data.get("retake", []) if retake_mode else data.get("available", [])

    if not courses:
        colored_print("No courses available.", "red")
        return

    title = "Retake List" if retake_mode else "Available Courses"
    print(f"\n--- {title} ---")
    for i, c in enumerate(courses, 1):
        print(f"{i}. {c['Code']} - {c['Name']} (Pre: {c['Prerequisites']})")

    idx = input("Select course number: ")
    if idx.isdigit() and 0 < int(idx) <= len(courses):
        code = courses[int(idx) - 1]["Code"]
        res = requests.post(
            f"{url}/enroll", json={"student_id": user["id"], "course_code": code}
        )
        if res.status_code == 200:
            colored_print("Enrolled!", "green")
            user["current_courses"].append(code)
        else:
            colored_print(res.json()["detail"], "red")


def drop_course(user):
    if not user["current_courses"]:
        colored_print("No active courses to drop.", "red")
        return

    print("\n--- Drop Course ---")
    for i, code in enumerate(user["current_courses"], 1):
        print(f"{i}. {code}")

    idx = input("Select course to drop: ")
    if idx.isdigit() and 0 < int(idx) <= len(user["current_courses"]):
        code = user["current_courses"][int(idx) - 1]
        res = requests.post(
            f"{url}/drop_course", json={"student_id": user["id"], "course_code": code}
        )
        if res.status_code == 200:
            colored_print("Dropped!", "green")
            user["current_courses"].remove(code)
        else:
            colored_print(res.json()["detail"], "red")


def upload_marks():
    sid = int(input("Student ID: "))
    code = input("Course Code: ")
    marks = int(input("Marks: "))

    res = requests.post(
        f"{url}/upload_marks",
        json={"student_id": sid, "course_code": code, "marks": marks},
    )
    if res.status_code == 200:
        colored_print(f"Done. GPA: {res.json()['gpa']}", "green")
    else:
        colored_print(res.json()["detail"], "red")


if __name__ == "__main__":
    big_print("Uni System")
    while True:
        print("\n--- MAIN MENU ---")
        c = get_choice(["Login", "Register", "Exit"])
        if c == "1":
            call_login()
        elif c == "2":
            call_register()
        elif c == "3":
            break
