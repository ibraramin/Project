from classes import BloodGroup, Student
import parsers

a = Student()

parsers.write_users(a)

print(parsers.load_users())


