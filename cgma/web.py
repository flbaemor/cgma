# filepath: /c:/Users/rmnxq/OneDrive/Desktop/csyr3/1st sem/o2eye/cgma-1/web/webapp.py
import streamlit as st
from cgmalexer import run

st.title("Lexer, Syntax, Semantic Analyzer")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Lexer", "Syntax", "Semantic"])

if page == "Lexer":
    st.header("Lexer")

    input_text = st.text_area("Enter code here:", height=200)

    if st.button("Run Lexer"):
        tokens, errors = run("<stdin>", input_text)

        st.subheader("Tokens")
        if tokens:
            for token in tokens:
                st.write(f"{token}")

        st.subheader("Errors")
        if errors:
            for error in errors:
                st.write(f"{error}")
        else:
            st.write("No errors found.")
elif page == "Syntax":
    st.header("Syntax Analyzer")
    st.write("Syntax analysis is not implemented yet.")
elif page == "Semantic":
    st.header("Semantic Analyzer")
    st.write("Semantic analysis is not implemented yet.")