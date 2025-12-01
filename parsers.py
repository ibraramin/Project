import os
import ast
from classes import Student, Faculty

user_file = "u.txt"
course_file = "c.txt"


def load_users() -> list:
    if not os.path.exists(user_file):
        return []

    users = []
    current_data = {}

    with open(user_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("id_") or line.startswith("ID:"):
                continue

            if line.startswith("[") and line.endswith("]"):
                if current_data:
                    users.append(create_user(current_data))
                current_data = {}
                continue

            if ":" in line:
                key, val = [x.strip() for x in line.split(":", 1)]
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1]
                    current_data[key] = (
                        [x.strip().strip("'\"") for x in inner.split(",")]
                        if inner
                        else []
                    )
                elif val.startswith("{") and val.endswith("}"):
                    try:
                        current_data[key] = ast.literal_eval(val)
                    except:
                        current_data[key] = {}
                else:
                    current_data[key] = None if val == "None" else val

    if current_data:
        users.append(create_user(current_data))
    return users


def get_user_index(users, id: int) -> int:
    for x, user in enumerate(users):
        if user.id == id:
            return x
    return -1


def get_user(id: int):
    for user in load_users():
        if user.id == id:
            return user
    return None


def create_user(data):
    conversions = {
        "id": int,
        "number": int,
        "semester": int,
        "salary": int,
        "gpa": float,
    }
    for k, func in conversions.items():
        if k in data and data[k] is not None:
            data[k] = func(data[k])

    if data.get("type") == "faculty":
        return Faculty(**data)
    return Student(**data)


def save_users(users):
    headers = ["id_student:0\n", "id_faculty:0\n"]
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                headers = lines[:2]

    with open(user_file, "w") as f:
        f.writelines(headers)
        f.write("\n")
        for i, u in enumerate(users, 1):
            f.write(f"[{i}]\n")
            for k, v in u.model_dump().items():
                if hasattr(v, "value"):
                    v = v.value
                f.write(f"{k}: {v}\n")
            f.write("\n")


def load_courses():
    if not os.path.exists(course_file):
        return []
    courses = []
    curr = {}

    with open(course_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("[") and line.endswith("]"):
                continue

            if line.startswith("Course Name:"):
                if curr:
                    courses.append(curr)
                curr = {"Name": line.split(":", 1)[1].strip()}
            elif "Code:" in line:
                curr["Code"] = line.split(":")[-1].strip()
            elif "Credits:" in line:
                curr["Credits"] = line.split(":")[-1].strip()
            elif "Prerequisites" in line:
                val = line.split("=" if "=" in line else ":")[1].strip()
                curr["Prerequisites"] = (
                    [] if "None" in val else [x.strip() for x in val.split(",")]
                )

        if curr:
            courses.append(curr)
    return courses


def validate_user(creds) -> bool:
    users = load_users()
    for user in users:
        if str(user.id) == str(creds["id"]) and str(user.password) == str(
            creds["password"]
        ):
            return True
    return False


def get_next_id_student():
    with open(user_file, "r") as f:
        lines = f.readlines()
    current_id_line = lines[0].strip()
    if ":" in current_id_line:
        curr = int(current_id_line.split(":")[-1])
    else:
        curr = 0

    new_id = curr + 1
    lines[0] = f"id_student:{new_id}\n"

    with open(user_file, "w") as f:
        f.writelines(lines)

    return new_id


def get_next_id_faculty():
    with open(user_file, "r") as f:
        lines = f.readlines()

    current_id_line = lines[1].strip()
    if ":" in current_id_line:
        curr = int(current_id_line.split(":")[-1])
    else:
        curr = 0
    new_id = curr + 1
    lines[1] = f"id_faculty:{new_id}\n"

    with open(user_file, "w") as f:
        f.writelines(lines)
    return new_id
