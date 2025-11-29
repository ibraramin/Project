import os
from classes import Student, Faculty, BloodGroup, Religion, Level, Department

u_file = "u.txt"
c_file = "c.txt"


def load_users() -> list:
    users = []

    if not os.path.exists(u_file):
        with open(u_file, "w") as f:
            f.write("ID:0\n")
        return []

    current_user_data = {}

    with open(u_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("ID:"):
            continue

        if line.startswith("[") and line.endswith("]"):

            if current_user_data:
                users.append(create_user_object(current_user_data))
            current_user_data = {}
            continue

        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip()

            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                if not inner:
                    current_user_data[key] = []
                else:

                    items = [
                        x.strip().replace("'", "").replace('"', "")
                        for x in inner.split(",")
                    ]
                    current_user_data[key] = items
            else:

                if val == "None":
                    current_user_data[key] = None
                else:
                    current_user_data[key] = val

    if current_user_data:
        users.append(create_user_object(current_user_data))

    return users


def create_user_object(data: dict):

    if "id" in data:
        data["id"] = int(data["id"])
    if "number" in data:
        data["number"] = int(data["number"])
    if "semester" in data:
        data["semester"] = int(data["semester"])
    if "salary" in data:
        data["salary"] = int(data["salary"])
    if "gpa" in data:
        data["gpa"] = float(data["gpa"])

    u_type = data.get("type", "student")
    try:
        if u_type == "faculty":
            return Faculty(**data)
        else:
            return Student(**data)
    except Exception as e:
        print(f"Error creating user object for {data.get('name')}: {e}")
        return Student(**data)


def save_users(users: list):

    max_id = 0
    if users:
        max_id = max((u.id for u in users if u.id is not None), default=0)

    with open(u_file, "w") as f:
        f.write(f"ID:{max_id}\n\n")

        for u in users:
            f.write(f"[{u.id}]\n")
            data = u.model_dump()
            for k, v in data.items():

                if hasattr(v, "value"):
                    v = v.value
                f.write(f"{k}: {v}\n")
            f.write("\n")


def populate() -> list:
    courses = []
    curr_course = None

    if not os.path.exists(c_file):
        return []

    with open(c_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Course Name:"):
                if curr_course is not None:
                    courses.append(curr_course)
                curr_course = {}
                parts = line.split()
                curr_course["Name"] = " ".join(parts[2:])

            if curr_course is not None:
                if line.startswith("Code:"):
                    curr_course["Code"] = line.split()[-1]
                elif line.startswith("Credits"):
                    curr_course["Credits"] = line.split()[-1]
                elif line.startswith("Prerequisites"):
                    if "None" in line:
                        curr_course["Prerequisites"] = []
                    else:
                        rhs = (
                            line.split("=")[1].strip()
                            if "=" in line
                            else line.split(":")[1].strip()
                        )
                        curr_course["Prerequisites"] = [
                            x.strip() for x in rhs.replace(",", " ").split()
                        ]

        if curr_course is not None:
            courses.append(curr_course)
    return courses
