import streamlit as st
from pypdf import PdfReader

st.title("📘 AI Study Assistant")

# -----------------------------
# PDF Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload study PDF (optional)", type="pdf")

def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -----------------------------
# Text Input
# -----------------------------
text = st.text_area("Paste your study text here")

if uploaded_file:
    text = extract_pdf_text(uploaded_file)
    st.success("PDF text extracted successfully")

# -----------------------------
# Quiz Options
# -----------------------------
difficulty = st.selectbox(
    "Select difficulty level",
    ["Easy", "Medium", "Hard"]
)

quiz_type = st.radio(
    "Select quiz type",
    ["MCQ", "True / False"]
)

# -----------------------------
# Progress Tracking
# -----------------------------
if "quiz_count" not in st.session_state:
    st.session_state.quiz_count = 0

# -----------------------------
# Generate Quiz
# -----------------------------
if st.button("Generate Quiz"):
    if text.strip() == "":
        st.warning("Please paste study text or upload a PDF")
    else:
        st.session_state.quiz_count += 1

        st.subheader(f"{difficulty} Level Quiz")

        if quiz_type == "MCQ":
            st.write("Q1. What is the main topic discussed?")
            st.write("a) Option A")
            st.write("b) Option B")
            st.write("c) Option C")
            st.write("d) Option D")

        else:
            st.write("Q1. The given text discusses an important topic.")
            st.write("True / False")

        st.info(f"Quizzes attempted: {st.session_state.quiz_count}")

# -----------------------------
# Flashcards
# -----------------------------
st.subheader("📒 Flashcards")

if text.strip() != "":
    st.write("Flashcard 1")
    st.write("Q: What is the topic?")
    st.write("A: Answer from the text")

    st.write("Flashcard 2")
    st.write("Q: One key point?")
    st.write("A: Answer from the text")