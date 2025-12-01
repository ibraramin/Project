from fastapi import FastAPI, HTTPException
from classes import Student, Faculty, MarksUpload
from parsers import *
from helper import calculate_gpa

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/courses")
def get_courses():
    return {"courses": load_courses()}


@app.get("/available_courses/{student_id}")
def get_available_courses(student_id: int):
    users = load_users()
    idx = get_user_index(users, student_id)
    if idx == -1:
        raise HTTPException(404, "Student not found")

    student = users[idx]
    all_courses = load_courses()
    available = []
    retake = []

    for c in all_courses:
        code = c["Code"]
        if code in student.current_courses:
            continue

        if code in student.past_courses:

            if code in student.results and student.results[code] <= 2.50:
                retake.append(c)
            continue

        prereqs = c["Prerequisites"]
        met_prereqs = True
        if prereqs:
            for p in prereqs:

                if p not in student.past_courses or student.results.get(p, 0.0) == 0.0:
                    met_prereqs = False
                    break

        if met_prereqs:
            available.append(c)

    return {"available": available, "retake": retake}


@app.post("/register/student", response_model=Student)
def register_student(student: Student):
    users = load_users()
    student.id = get_next_id_student()
    users.append(student)
    save_users(users)
    return student


@app.post("/register/faculty", response_model=Faculty)
def register_faculty(faculty: Faculty):
    users = load_users()
    faculty.id = get_next_id_faculty()
    users.append(faculty)
    save_users(users)
    return faculty


@app.post("/login")
def login(creds: dict):
    users = load_users()
    user = None
    for u in users:
        if str(u.id) == str(creds["id"]) and str(u.password) == str(creds["password"]):
            user = u
            break

    if not user:
        raise HTTPException(404, "Wrong Id or Password, please try again.")

    return {"status": "success", "user": user.model_dump()}


@app.put("/user/{user_id}")
def update_user(user_id: int, user_update_data: dict):
    users = load_users()

    index = get_user_index(users, user_id)
    if index == -1:
        raise HTTPException(404, "User not found")

    current_user = users[index]
    updated_user = current_user.model_copy(update=user_update_data)
    users[index] = updated_user
    save_users(users)
    return {"status": "updated", "data": updated_user}


@app.post("/enroll")
def enroll(data: dict):
    users = load_users()
    student_index = get_user_index(users, int(data["student_id"]))

    if student_index == -1:
        raise HTTPException(404, "Student not found")

    student = users[student_index]

    if data["course_code"] in student.current_courses:
        raise HTTPException(400, "You are already enrolled in this course")

    student.current_courses.append(data["course_code"])
    save_users(users)
    return {"status": "success", "data": student}


@app.post("/drop_course")
def drop_course(data: dict):
    users = load_users()
    idx = get_user_index(users, int(data["student_id"]))
    if idx == -1:
        raise HTTPException(404, "Student not found")

    student = users[idx]
    if data["course_code"] in student.current_courses:
        student.current_courses.remove(data["course_code"])
        save_users(users)
        return {"status": "success"}

    raise HTTPException(400, "Course not found in current list")


@app.post("/upload_marks")
def upload_marks(data: MarksUpload):
    users = load_users()
    student_index = get_user_index(users, data.student_id)

    if student_index == -1:
        raise HTTPException(404, "Student not found")

    student = users[student_index]

    if data.course_code not in student.current_courses:
        raise HTTPException(400, "You are not enrolled in this course")

    point = calculate_gpa(data.marks)
    student.results[data.course_code] = point

    student.current_courses.remove(data.course_code)
    if data.course_code not in student.past_courses:
        student.past_courses.append(data.course_code)

    if student.results:
        student.gpa = round(sum(student.results.values()) / len(student.results), 2)

    save_users(users)
    return {"status": "success", "gpa": point, "cgpa": student.gpa}
