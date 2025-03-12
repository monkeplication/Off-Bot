# Off-Bot
Off-Bot is a Student Management System designed for tutors to manage student data, exam datesheets, leave applications, and generate certificates. It also features a data-driven chat interface for querying student-related information.

## Features
- Manage Student Records
- Create and View Exam Datesheets
- Handle Leave Applications
- Generate Certificates (Bonafide, NOC, Internship Completion)
- Chat with Data

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Database: Postgre
- PDF Generation for Certificates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/monkeplication/Off-Bot.git
cd Off-Bot
```

2. Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the backend:
```bash
uvicorn backend.codebaseai:app --reload
```

2. Run the frontend:
```bash
streamlit run app.py
```

## API Endpoints
- `GET /students/` - Fetch all students
- `POST /students/` - Add a new student
- `PUT /students/{student_id}` - Update student information
- `DELETE /students/{student_id}` - Delete a student
- `GET /datesheets/` - Fetch all exam datesheets
- `POST /datesheets/` - Add a new exam datesheet
- `GET /leave_applications/` - Fetch all leave applications
- `POST /leave_applications/` - Submit a leave application
- `POST /generate_certificate/` - Generate a certificate
- `POST /chat_with_data/` - Chat with data

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Author
[monkeplication](https://github.com/monkeplication)
