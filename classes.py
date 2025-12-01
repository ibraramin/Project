from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class BloodGroup(str, Enum):
    a_pos = "a+"
    a_neg = "a-"
    b_pos = "b+"
    b_neg = "b-"
    o_pos = "o+"
    o_neg = "o-"
    ab_pos = "ab+"
    ab_neg = "ab-"
    pending = "pending"


class Religion(str, Enum):
    islam = "Islam"
    christianity = "Christianity"
    hinduism = "Hinduism"
    buddhism = "Buddhism"
    atheism = "Atheism"
    pending = "pending"


class Level(str, Enum):
    lecturer = "Lecturer"
    assoc_prof = "Associate Professor"
    assist_prof = "Assistant Professor"
    professor = "Professor"
    head = "Head"
    pending = "pending"


class Department(str, Enum):
    cs = "Computer Science"
    ba = "Business Administration"
    arts = "Arts and Humanities"
    law = "Department of Law"
    pending = "pending"


class User(BaseModel):
    id: Optional[int] = None
    password: str = "default"
    name: str = "default"
    address: str = "pending"
    number: int = 0
    email: str = "pending"
    dob: str = "2000-01-01"
    blood_group: BloodGroup = BloodGroup.pending
    religion: Religion = Religion.pending
    type: str = "user"
    pfp: str = "pfps/default.jpeg"


class Student(User):
    type: str = "student"
    semester: int = 1
    gpa: float = 0.0
    dept: Department = Department.pending
    current_courses: List[str] = Field(default_factory=list)
    past_courses: List[str] = Field(default_factory=list)
    results: Dict[str, float] = Field(default_factory=dict)


class Faculty(User):
    type: str = "faculty"
    salary: int = 0
    level: Level = Level.pending
    dept: Department = Department.pending


class MarksUpload(BaseModel):
    student_id: int
    course_code: str
    marks: int
