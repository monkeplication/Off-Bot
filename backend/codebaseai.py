from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models as models
import schemas as schemas
from fpdf import FPDF


load_dotenv() # load keys
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    task: str
    query: str

# Chatbot endpoints
@app.post("/chat/")
async def chatbot(request: ChatRequest):
    prompt = f"Task: {request.task}\nQuery: {request.query}\nAnswer:"
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        return {"task": request.task, "answer": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Student endpoints
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

# Exam datesheet endpoints
@app.post("/datesheets/", response_model=schemas.ExamDatesheet)
def create_datesheet(datesheet: schemas.ExamDatesheetCreate, db: Session = Depends(get_db)):
    # Ensure the student exists before adding datesheet
    student = db.query(models.Student).filter(models.Student.id == datesheet.student_id).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student ID not found")

    db_datesheet = models.ExamDatesheet(**datesheet.dict())
    db.add(db_datesheet)
    db.commit()
    db.refresh(db_datesheet)
    return db_datesheet

@app.get("/datesheets/", response_model=list[schemas.ExamDatesheet])
def read_datesheets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datesheets = db.query(models.ExamDatesheet).offset(skip).limit(limit).all()
    return datesheets

@app.get("/datesheets/{datesheet_id}", response_model=schemas.ExamDatesheet)
def read_datesheet(datesheet_id: int, db: Session = Depends(get_db)):
    datesheet = db.query(models.ExamDatesheet).filter(models.ExamDatesheet.id == datesheet_id).first()
    if datesheet is None:
        raise HTTPException(status_code=404, detail="Exam datesheet not found")
    return datesheet

@app.put("/datesheets/{datesheet_id}", response_model=schemas.ExamDatesheet)
def update_datesheet(datesheet_id: int, datesheet: schemas.ExamDatesheetUpdate, db: Session = Depends(get_db)):
    db_datesheet = db.query(models.ExamDatesheet).filter(models.ExamDatesheet.id == datesheet_id).first()
    if db_datesheet is None:
        raise HTTPException(status_code=404, detail="Exam datesheet not found")
    
    for key, value in datesheet.dict(exclude_unset=True).items():
        setattr(db_datesheet, key, value)
    
    db.commit()
    db.refresh(db_datesheet)
    return db_datesheet

@app.delete("/datesheets/{datesheet_id}")
def delete_datesheet(datesheet_id: int, db: Session = Depends(get_db)):
    datesheet = db.query(models.ExamDatesheet).filter(models.ExamDatesheet.id == datesheet_id).first()
    if datesheet is None:
        raise HTTPException(status_code=404, detail="Exam datesheet not found")
    
    db.delete(datesheet)
    db.commit()
    return {"message": "Exam datesheet deleted successfully"}

@app.post("/leave_applications/", response_model=schemas.LeaveApplication)
def create_leave_application(leave_application: schemas.LeaveApplicationCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == leave_application.student_id).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student ID not found")

    db_leave_application = models.LeaveApplication(**leave_application.dict())
    db.add(db_leave_application)
    db.commit()
    db.refresh(db_leave_application)
    return db_leave_application

@app.get("/leave_applications/", response_model=list[schemas.LeaveApplication])
def read_leave_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leave_applications = db.query(models.LeaveApplication).offset(skip).limit(limit).all()
    return leave_applications

@app.get("/leave_applications/{leave_application_id}", response_model=schemas.LeaveApplication)
def read_leave_application(leave_application_id: int, db: Session = Depends(get_db)):
    leave_application = db.query(models.LeaveApplication).filter(models.LeaveApplication.id == leave_application_id).first()
    if leave_application is None:
        raise HTTPException(status_code=404, detail="Leave application not found")
    return leave_application

@app.put("/leave_applications/{leave_application_id}", response_model=schemas.LeaveApplication)
def update_leave_application(leave_application_id: int, leave_application: schemas.LeaveApplicationUpdate, db: Session = Depends(get_db)):
    db_leave_application = db.query(models.LeaveApplication).filter(models.LeaveApplication.id == leave_application_id).first()
    if db_leave_application is None:
        raise HTTPException(status_code=404, detail="Leave application not found")
    
    for key, value in leave_application.dict(exclude_unset=True).items():
        setattr(db_leave_application, key, value)
    
    db.commit()
    db.refresh(db_leave_application)
    return db_leave_application

@app.delete("/leave_applications/{leave_application_id}")
def delete_leave_application(leave_application_id: int, db: Session = Depends(get_db)):
    leave_application = db.query(models.LeaveApplication).filter(models.LeaveApplication.id == leave_application_id).first()
    if leave_application is None:
        raise HTTPException(status_code=404, detail="Leave application not found")
    
    db.delete(leave_application)
    db.commit()
    return {"message": "Leave application deleted successfully"}

@app.post("/chat_with_data/")
async def chat_with_data(request: ChatRequest, db: Session = Depends(get_db)):

    # Extract query and task
    query = request.query.lower()
    task = request.task.lower()

    # Fetch student data
    if "student" in query or "student" in task:
        students = db.query(models.Student).all()
        student_info = "\n".join([f"{s.name}, ID: {s.student_id}, Program: {s.program}, Semester: {s.semester}" for s in students])
    else:
        student_info = "No student data requested."

    # Fetch exam datesheet data
    if "exam" in query or "datesheet" in task:
        datesheets = db.query(models.ExamDatesheet).all()
        datesheet_info = "\n".join([f"{d.subject} on {d.exam_date} from {d.start_time} to {d.end_time} at {d.location}" for d in datesheets])
    else:
        datesheet_info = "No datesheet data requested."

    # Create prompt with fetched data
    prompt = f"Task: {request.task}\nQuery: {request.query}\nStudent Data:\n{student_info}\nExam Datesheet Data:\n{datesheet_info}\nAnswer:"

    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        return {"task": request.task, "answer": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_certificate/")
def generate_certificate(request: schemas.CertificateRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    cert_type = request.cert_type
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Certificate of " + cert_type, ln=True, align="C")
    pdf.ln(20)
    pdf.cell(200, 10, txt=f"This is to certify that {student.name} with ID {student.student_id} is a student of {student.program} in semester {student.semester}.", ln=True, align="L")

    output_path = f"{cert_type}_Certificate_{student.student_id}.pdf"
    pdf.output(output_path)

    return {"message": "Certificate generated successfully", "certificate_path": output_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # Add student before adding datesheet