import streamlit as st
import requests
import pandas as pd

# Backend URL
BASE_URL = "http://localhost:8000"

st.title("Student Management System for Tutors")

menu = st.sidebar.selectbox("Menu", ["Manage Students", "Manage Exam Datesheets", "Manage Leave Applications", "Generate Certificates", "Chat with Data"])

if menu == "Manage Students":
    st.header("Manage Students")
    if st.button("Fetch Students"):
        response = requests.get(f"{BASE_URL}/students/")
        if response.status_code == 200:
            students = response.json()
            st.write(pd.DataFrame(students))
        else:
            st.error("Failed to fetch students")
    
    # Add Student
    st.subheader("Add Student")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    program = st.text_input("Program")
    semester = st.number_input("Semester", min_value=1, step=1)
    if st.button("Add Student"):
        payload = {"name": name, "email": email, "student_id": student_id, "program": program, "semester": semester}
        response = requests.post(f"{BASE_URL}/students/", json=payload)
        if response.status_code == 200:
            st.success("Student added successfully")
        else:
            st.error("Failed to add student")

    # Update Student
    st.subheader("Update Student")
    update_id = st.number_input("Student ID to Update", min_value=1, step=1)
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_program = st.text_input("New Program")
    new_semester = st.number_input("New Semester", min_value=1, step=1)
    if st.button("Update Student"):
        payload = {"name": new_name, "email": new_email, "program": new_program, "semester": new_semester}
        response = requests.put(f"{BASE_URL}/students/{update_id}", json=payload)
        if response.status_code == 200:
            st.success("Student updated successfully")
        else:
            st.error("Failed to update student")

    # Delete Student
    st.subheader("Delete Student")
    delete_id = st.number_input("Student ID to Delete", min_value=1, step=1)
    if st.button("Delete Student"):
        response = requests.delete(f"{BASE_URL}/students/{delete_id}")
        if response.status_code == 200:
            st.success("Student deleted successfully")
        else:
            st.error("Failed to delete student")

if menu == "Manage Exam Datesheets":
    st.header("Manage Exam Datesheets")
    if st.button("Fetch Exam Datesheets"):
        response = requests.get(f"{BASE_URL}/datesheets/")
        if response.status_code == 200:
            datesheets = response.json()
            st.write(pd.DataFrame(datesheets))
        else:
            st.error("Failed to fetch exam datesheets")

    # Add Exam Datesheet
    st.subheader("Add Exam Datesheet")
    student_id = st.number_input("Student ID", min_value=1, step=1)
    subject = st.text_input("Subject")
    exam_date = st.date_input("Exam Date")
    start_time = st.text_input("Start Time")
    end_time = st.text_input("End Time")
    location = st.text_input("Location")
    notes = st.text_area("Notes")
    if st.button("Add Exam Datesheet"):
        payload = {"student_id": student_id, "subject": subject, "exam_date": str(exam_date), "start_time": start_time, "end_time": end_time, "location": location, "notes": notes}
        response = requests.post(f"{BASE_URL}/datesheets/", json=payload)
        if response.status_code == 200:
            st.success("Exam Datesheet added successfully")
        else:
            st.error("Failed to add exam datesheet")

if menu == "Manage Leave Applications":
    st.header("Manage Leave Applications")
    if st.button("Fetch Leave Applications"):
        response = requests.get(f"{BASE_URL}/leave_applications/")
        if response.status_code == 200:
            leave_applications = response.json()
            st.write(pd.DataFrame(leave_applications))
        else:
            st.error("Failed to fetch leave applications")

    # Add Leave Application
    student_id = st.number_input("Student ID", min_value=1, step=1)
    reason = st.text_area("Reason")
    status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
    if st.button("Submit Leave Application"):
        payload = {"student_id": student_id, "reason": reason, "status": status}
        response = requests.post(f"{BASE_URL}/leave_applications/", json=payload)
        if response.status_code == 200:
            st.success("Leave application submitted successfully")
        else:
            st.error("Failed to submit leave application")

if menu == "Generate Certificates":
    st.header("Generate Certificates")
    cert_student_id = st.text_input("Student ID")
    cert_type = st.selectbox("Certificate Type", ["Bonafide", "NOC", "Internship Completion"])
    if st.button("Generate Certificate"):
        payload = {"student_id": cert_student_id, "cert_type": cert_type}
        response = requests.post(f"{BASE_URL}/generate_certificate/", json=payload)
        if response.status_code == 200:
            st.success("Certificate generated successfully")
            st.download_button("Download Certificate", response.content, f"{cert_type}_Certificate.pdf")
        else:
            st.error("Failed to generate certificate")

if menu == "Chat with Data":
    st.header("Chat with Data")
    task = st.text_input("Enter the task")
    query = st.text_area("Enter your query")
    if st.button("Ask"):
        payload = {"task": task, "query": query}
        response = requests.post(f"{BASE_URL}/chat_with_data/", json=payload)
        if response.status_code == 200:
            st.write(response.json().get("answer", "No response received."))
        else:
            st.error("Failed to get a response from the server")
