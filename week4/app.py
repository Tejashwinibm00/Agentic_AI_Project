import streamlit as st
from PyPDF2 import PdfReader

st.title("AI Study Assistant – Week 4")

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

st.text_area("Or paste study text here", value=text, height=200)

# -------------------------------
# DIFFICULTY LEVEL
# -------------------------------
difficulty = st.selectbox(
    "Choose difficulty level",
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
            questions.append(q)

        elif level == "Medium":
            q = f"What is meant by: {s}?"
            questions.append(q)

        elif level == "Hard":
            words = s.split()
            if len(words) > 4:
                words[2] = "______"
                q = "Fill in the blank: " + " ".join(words)
                questions.append(q)

        if len(questions) == 5:
            break

    return questions

# -------------------------------
# FLASHCARDS
# -------------------------------
def generate_flashcards(content):
    cards = []
    sentences = content.split(".")

    for s in sentences:
        s = s.strip()
        if len(s) > 20:
            cards.append(s)
        if len(cards) == 5:
            break

    return cards

# -------------------------------
# BUTTON ACTION
# -------------------------------
if st.button("Generate Quiz"):
    if text.strip() == "":
        st.warning("Please upload or paste study text")
    else:
        quiz = generate_quiz(text, difficulty)

        st.subheader("Quiz Questions")
        for i, q in enumerate(quiz, 1):
            st.write(f"{i}. {q}")

        st.info(f"Total Questions: {len(quiz)}")
        st.info(f"Difficulty Level: {difficulty}")

        st.subheader("Flashcards")
        flashcards = generate_flashcards(text)
        for card in flashcards:
            with st.expander("Show Flashcard"):
                st.write(card)