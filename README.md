```
  OOO   FFFFF  FFFFF   BBBB   OOO   TTTTT
 O   O  F      F      B   B  O   O    T  
 O   O  FFF    FFF    BBBB   O   O    T  
 O   O  F      F      B   B  O   O    T  
  OOO   F      F      BBBB    OOO     T  
```

# Off-Bot

**Student Management System**

A simple yet powerful tool for tutors to manage student records, exam datesheets, leave applications, and certificate generation. Features a chat interface to interact with data effortlessly.

## 🚀 Features
- Manage Student Records
- Exam Datesheet Management
- Leave Application Handling
- Certificate Generation
- Data-Driven Chat Interface

## 🛠 Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** SQLite
- **PDF Generation:** fpdf

## 📦 Installation

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

4. Set up environment variables: Create a `.env` file in the root directory and add the following:

```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/<DB-Name>
```

## 📌 Usage:

1. Run the backend:
```bash
uvicorn backend.main:app --reload
```

2. Run the frontend:
```bash
streamlit run frontend/app.py
```

## 📬 Connect with Me
- GitHub: [monkeplication](https://github.com/monkeplication)

---

