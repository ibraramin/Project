from fastapi import FastAPI, HTTPException
from typing import Union
from classes import Student, Faculty, User
import parsers

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "University System API is running"}


def get_next_id(users):
    if not users:
        return 1

    ids = [u.id for u in users if u.id is not None]
    if not ids:
        return 1
    return max(ids) + 1


@app.post("/register/student", response_model=Student)
def register_student(student: Student):
    users = parsers.load_users()
    student.id = get_next_id(users)
    student.type = "student"
    users.append(student)
    parsers.save_users(users)
    return student


@app.post("/register/faculty", response_model=Faculty)
def register_faculty(faculty: Faculty):
    users = parsers.load_users()
    faculty.id = get_next_id(users)
    faculty.type = "faculty"
    users.append(faculty)
    parsers.save_users(users)
    return faculty


@app.post("/login")
def login(data: dict):
    users = parsers.load_users()
    user_id = data.get("id")
    password = data.get("password")

    for u in users:
        if u.id == user_id:
            if u.password == password:
                return {
                    "status": "success",
                    "message": f"Welcome {u.name}",
                    "user": u.model_dump(),
                }
            else:
                raise HTTPException(status_code=401, detail="Wrong Password")

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/update/user/{user_id}")
def update_user(user_id: int, updated_data: dict):
    users = parsers.load_users()
    found = False
    updated_user = None

    for i, u in enumerate(users):
        if u.id == user_id:

            current_data = u.model_dump()

            current_data.update(updated_data)

            if u.type == "student":
                users[i] = Student(**current_data)
            else:
                users[i] = Faculty(**current_data)

            updated_user = users[i]
            found = True
            break

    if not found:
        raise HTTPException(404, "User not found")

    parsers.save_users(users)
    return {"status": "updated", "data": updated_user}
