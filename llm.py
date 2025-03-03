import os
import streamlit as st
from groq import Groq
import json
from pygments import highlight
from pygments.lexers import PythonLexer, JavascriptLexer, CppLexer, JavaLexer
from pygments.formatters import HtmlFormatter

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ API Key not found. Please set the 'GROQ_API_KEY' environment variable.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

def call_groq_api(code_snippet, language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an advanced AI coding expert. Analyze, debug, and optimize the provided code."},
                {"role": "user", "content": f"Analyze and fix this {language} code:\n```{code_snippet}```"},
            ],
            model="mixtral-8x7b-32768", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error calling Groq API: {e}"

def explain_code_fix(original_code, fixed_code, language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI that explains code improvements."},
                {"role": "user", "content": f"Explain the improvements made to this {language} code:\n\nOriginal:\n```{original_code}```\n\nFixed:\n```{fixed_code}```"},
            ],
            model="mixtral-8x7b-32768",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error explaining code: {e}"

def grade_code(code_snippet, language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI that evaluates code quality on a scale from 1 to 10."},
                {"role": "user", "content": f"Rate this {language} code for quality, efficiency, and best practices:\n```{code_snippet}```"},
            ],
            model="mixtral-8x7b-32768",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error grading code: {e}"

st.set_page_config(page_title="🚀 AI Code Fixer & Optimizer", page_icon="🐞", layout="wide")

st.title("CodeDoctor")
st.subheader("he AI that diagnoses and heals your buggy code!")

language = st.selectbox("🛠️ Select Programming Language", ["Python", "JavaScript", "C++", "Java"])
user_code = st.text_area("🔽 Paste your code below:", height=250)

if st.button("✨ Fix & Optimize Code"):
    if user_code.strip():
        with st.spinner("🛠️ AI is analyzing your code..."):
            fixed_code = call_groq_api(user_code, language)

        with st.spinner("📖 AI is explaining the fixes..."):
            explanation = explain_code_fix(user_code, fixed_code, language)

        with st.spinner("📊 AI is grading your code..."):
            grade = grade_code(user_code, language)

        st.subheader("Optimized & Fixed Code")

        lexer = {
            "Python": PythonLexer(),
            "JavaScript": JavascriptLexer(),
            "C++": CppLexer(),
            "Java": JavaLexer()
        }.get(language, PythonLexer())

        st.code(fixed_code, language=language.lower())

        st.subheader("📖 AI Explanation")
        st.write(explanation)

        st.subheader("📊 AI Code Rating")
        st.write(grade)

        st.download_button(label="💾 Download Fixed Code",
                           data=fixed_code,
                           file_name=f"fixed_code.{language.lower()}",
                           mime="text/plain")
    else:
        st.warning("⚠️ Please enter some code before clicking Fix & Optimize.")

st.markdown("**Built with ❤️ by Ankan Moh.**")