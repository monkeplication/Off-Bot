# To check contents of the DB currently ( just made this for me , no need to use if you don't want and I was new with PostgreSQL so , tried this)

from database import SessionLocal
from models import Student, ExamDatesheet

db = SessionLocal()

# Fetch and print all students int the Table
students = db.query(Student).all()
print("Students:")
for student in students:
    print(f"Name: {student.name}, Email: {student.email}, Program: {student.program}, Semester: {student.semester}")

# Fetch and print all exam datesheets in the Table
datesheets = db.query(ExamDatesheet).all()
print("\nExam Datesheets:")
for datesheet in datesheets:
    print(f"Subject: {datesheet.subject}, Date: {datesheet.exam_date}, Location: {datesheet.location}")

db.close()
