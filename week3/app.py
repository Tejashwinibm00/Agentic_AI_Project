import streamlit as st
from pypdf import PdfReader

st.title("AI Study Assistant")

uploaded_file = st.file_uploader("Upload study PDF (optional)", type="pdf")

def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

text = st.text_area("Paste your study text here")

if uploaded_file:
    text = extract_pdf_text(uploaded_file)
    st.success("PDF text extracted successfully")

# WEEK 3: QUIZ GENERATOR
# ----------------------------

st.subheader("Week 3: Quiz Generator")

difficulty = st.selectbox(
    "Choose difficulty level",
    ["Easy", "Medium", "Hard"]
)

def generate_quiz(text, difficulty):
    questions = []
    sentences = text.split(".")

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:
            questions.append("What is meant by: " + sentence + "?")

    if difficulty == "Easy":
        return questions[:3]
    elif difficulty == "Medium":
        return questions[:5]
    else:
        return questions[:7]

if st.button("Generate Quiz"):
    if text:
        quiz_questions = generate_quiz(text, difficulty)

        st.subheader("Generated Questions")
        for i, q in enumerate(quiz_questions, 1):
            st.write(f"{i}. {q}")
    else:
        st.warning("Please upload a PDF or paste text first")