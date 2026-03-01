import streamlit as st

st.title("AI Study Assistant")

text = st.text_area("Paste your study text here")

if st.button("Generate Quiz"):
    if text.strip() == "":
        st.warning("Please paste some study text")
    else:
        st.subheader("Generated Quiz")

        st.write("Q1. What is the topic discussed in the text?")
        st.write("Q2. Explain the topic in short.")
        st.write("Q3. Write one advantage or use.")