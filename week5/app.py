import streamlit as st
import sqlite3
from PyPDF2 import PdfReader

st.title("AI Study Assistant – Week 5")

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("study.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    difficulty TEXT,
    questions INTEGER
)
""")
conn.commit()

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload study file (PDF or TXT)",
    type=["pdf", "txt"]
)

text = ""

def extract_pdf_text(file):
    reader = PdfReader(file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_pdf_text(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

text = st.text_area("Or paste study text here", value=text, height=200)

# -------------------------------
# SUBJECT & DIFFICULTY
# -------------------------------
subject = st.selectbox(
    "Choose Subject",
    ["Python", "DBMS", "Operating System", "Data Structures", "General"]
)

difficulty = st.selectbox(
    "Choose Difficulty",
    ["Easy", "Medium", "Hard"]
)

# -------------------------------
# QUIZ GENERATOR
# -------------------------------
def generate_quiz(content, level):
    questions = []
    sentences = content.split(".")

    for s in sentences:
        s = s.strip()
        if len(s) < 20:
            continue

        if level == "Easy":
            q = f"True or False: {s}"

        elif level == "Medium":
            q = f"What is meant by: {s}?"

        else:
            words = s.split()
            if len(words) > 4:
                words[2] = "______"
            q = "Fill in the blank: " + " ".join(words)

        questions.append(q)

        if len(questions) == 5:
            break

    return questions

# -------------------------------
# BUTTON
# -------------------------------
if st.button("Generate Quiz"):
    if text.strip() == "":
        st.warning("Please upload or paste study text")
    else:
        quiz = generate_quiz(text, difficulty)

        st.subheader("Quiz Questions")
        for i, q in enumerate(quiz, 1):
            st.write(f"{i}. {q}")

        # SAVE PROGRESS
        c.execute(
            "INSERT INTO progress (subject, difficulty, questions) VALUES (?, ?, ?)",
            (subject, difficulty, len(quiz))
        )
        conn.commit()

        st.success("Study progress saved!")

        # STUDY SUGGESTION
        st.subheader("Study Suggestion")
        if difficulty == "Easy":
            st.info("You are doing well. Try Medium level next.")
        elif difficulty == "Medium":
            st.info("Good progress. Revise once and try Hard level.")
        else:
            st.warning("Hard level chosen. Revise basics for better understanding.")

# -------------------------------
# SHOW PROGRESS
# -------------------------------
st.subheader("Your Study Progress")

c.execute("SELECT subject, COUNT(*) FROM progress GROUP BY subject")
rows = c.fetchall()

if rows:
    for row in rows:
        st.write(f"{row[0]} quizzes attempted: {row[1]}")
else:
    st.write("No study progress yet.")