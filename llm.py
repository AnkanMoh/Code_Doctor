import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_PAT")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GITHUB_TOKEN:
    st.error("❌ GitHub API Token not found. Set 'GITHUB_PAT' in your .env file.")
    st.stop()
if not GROQ_API_KEY:
    st.error("❌ Groq API Key not found. Set 'GROQ_API_KEY' in your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Code-Doctor : AI GitHub Bug Fixer", page_icon="🐙", layout="wide")

st.markdown("""
    <style>
        .big-font { font-size:20px !important; }
        .stMarkdown { font-size:18px; font-weight:bold; }
        .fixed-code { background-color: #282C34; color: #ABB2BF; padding: 10px; border-radius: 5px; font-family: 'Courier New', monospace; }
        .issue-card { background-color: #F0F0F0; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .issue-title { font-size: 20px; font-weight: bold; color: #E63946; }
        .file-path { font-weight: bold; color: #457B9D; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color:#1D3557;'>FixGenie: AI-driven bug fixer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color:#457B9D;'>Debugging made easy.</h4>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

github_url = st.text_input("🔗 Enter GitHub Repository Link:", placeholder="https://github.com/user/repo")

def extract_repo_details(github_url):
    parts = github_url.rstrip("/").split("/")
    if len(parts) < 2:
        return None, None
    return parts[-2], parts[-1]

def fetch_github_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def fetch_repo_files(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    return [file['path'] for file in response.json() if 'path' in file and file['type'] == 'file'] if response.status_code == 200 else []

def extract_file_path(issue_body, repo_files):
    valid_extensions = [".py", ".cpp", ".js", ".c", ".java"]
    if not issue_body or not repo_files:
        return None

    for line in issue_body.split("\n"):
        for repo_file in repo_files:
            if line.strip() in repo_file and any(repo_file.endswith(ext) for ext in valid_extensions):
                return repo_file
    return None

# 🔹 Fetch file content from GitHub
def fetch_buggy_code(owner, repo, file_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    return base64.b64decode(response.json()["content"]).decode("utf-8") if response.status_code == 200 else None

# 🔹 AI-Powered Code Fixing with Detailed Explanation
def fix_code_with_ai(code_snippet, language):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert AI software engineer. Your task is to debug and optimize code with clear explanations. "
                                              "For each fix, provide the following details:\n"
                                              "1. **Root Cause:** Explain why the bug occurs.\n"
                                              "2. **Fixed Code:** Provide the corrected code in a proper format.\n"
                                              "3. **Explanation:** Clearly explain what was fixed and why, in a professional manner.\n"
                                              "Ensure responses are structured and polished."},
                {"role": "user", "content": f"Debug and optimize this {language} code:\n```{code_snippet}```"},
            ],
            model="mixtral-8x7b-32768",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ AI Error: {e}")
        return None

if st.button("🔍 Fetch Issues & Fix Bugs"):
    if github_url.strip():
        owner, repo = extract_repo_details(github_url)
        with st.spinner("📡 Fetching GitHub issues..."):
            issues = fetch_github_issues(owner, repo)

        if issues:
            repo_files = fetch_repo_files(owner, repo)  
            st.subheader("Opening GitHub Issues (With Valid File Paths)")

            filtered_issues = []
            for issue in issues:
                file_path = extract_file_path(issue["body"], repo_files)
                if file_path:
                    filtered_issues.append({"title": issue["title"], "body": issue["body"], "file_path": file_path})

            if filtered_issues:
                for issue in filtered_issues:
                    st.markdown(f"<div class='issue-card'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='issue-title'>🔹 {issue['title']}</p>", unsafe_allow_html=True)
                    st.write(issue["body"])
                    st.markdown(f"<p class='file-path'>✅ Matched File: `{issue['file_path']}`</p>", unsafe_allow_html=True)

                    with st.spinner("📡 Fetching source code..."):
                        buggy_code = fetch_buggy_code(owner, repo, issue["file_path"])

                    if buggy_code:
                        with st.spinner("🤖 AI is generating a fix..."):
                            fixed_code = fix_code_with_ai(buggy_code, "Python")

                        if fixed_code:
                            st.subheader(" AI-Generated Fix Report")
                            sections = fixed_code.split("\n\n")  
                            for section in sections:
                                if "**Root Cause:**" in section:
                                    st.markdown(f"### Root Cause\n{section.replace('**Root Cause:**', '').strip()}", unsafe_allow_html=True)
                                elif "**Fixed Code:**" in section:
                                    st.subheader("Fixed Code")
                                    st.code(section.replace('**Fixed Code:**', '').strip(), language="python")
                                elif "**Explanation:**" in section:
                                    st.markdown(f"### Explanation\n{section.replace('**Explanation:**', '').strip()}", unsafe_allow_html=True)
                        else:
                            st.error("❌ AI could not generate a fix.")
                    else:
                        st.error(f"❌ Could not fetch `{issue['file_path']}` from the repository.")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No issues found with valid file paths.")

st.markdown("**Built with ❤️ by Ankan Moh.**")
