from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    student_id = Column(String, unique=True, index=True)
    program = Column(String)
    semester = Column(Integer)
    
    # Relationship with ExamDatesheet
    datesheets = relationship("ExamDatesheet", back_populates="student")
    
    # Relationship with LeaveApplication
    leave_applications = relationship("LeaveApplication", back_populates="student")

class ExamDatesheet(Base):
    __tablename__ = "exam_datesheets"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, index=True)
    exam_date = Column(Date)
    start_time = Column(String)
    end_time = Column(String)
    location = Column(String)
    notes = Column(Text, nullable=True)
    
    # Relationship with Student
    student = relationship("Student", back_populates="datesheets")
    
class LeaveApplication(Base):
    __tablename__ = "leave_applications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    reason = Column(Text, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="leave_applications")
