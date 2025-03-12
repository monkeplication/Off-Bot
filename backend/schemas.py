#Schemas in the Database

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from datetime import datetime

# Student schemas
class StudentBase(BaseModel):
    name: str
    email: str
    student_id: str
    program: str
    semester: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    program: Optional[str] = None
    semester: Optional[int] = None

# ExamDatesheet schemas
class ExamDatesheetBase(BaseModel):
    student_id: int
    subject: str
    exam_date: date
    start_time: str
    end_time: str
    location: str
    notes: Optional[str] = None

class ExamDatesheetCreate(ExamDatesheetBase):
    pass

class ExamDatesheetUpdate(BaseModel):
    subject: Optional[str] = None
    exam_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class ExamDatesheet(ExamDatesheetBase):
    id: int
    
    model_config = {
    "from_attributes": True
}

class Student(StudentBase):
    id: int
    datesheets: List[ExamDatesheet] = []
    
    class Config:
        orm_mode = True

class LeaveApplicationBase(BaseModel):
    student_id: int
    reason: str
    start_date: datetime
    end_date: datetime
    status: Optional[str] = "Pending"

class LeaveApplicationCreate(LeaveApplicationBase):
    pass

class LeaveApplicationUpdate(BaseModel):
    reason: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[str]

class LeaveApplication(LeaveApplicationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CertificateRequest(BaseModel):
    student_id: int
    cert_type: str
