🪄 FixGenie – AI-Powered Bug Fixer & Optimizer 🚀

Your Ultimate AI Coding Assistant for Debugging & Optimization

📌 Overview

FixGenie is an AI-powered bug fixer and code optimizer that uses Groq’s mixtral-8x7b-32768 model to:
✅ Identify and fix coding errors
✅ Optimize performance
✅ Explain fixes in plain English
✅ Evaluate code quality
✅ Support multiple programming languages

FixGenie helps developers debug and improve their code instantly, making it a powerful tool for software engineers, students, and AI enthusiasts.

🚀 Features

🔹 AI Bug Detection & Fixes – Automatically detects and corrects syntax & logic errors.
🔹 Performance Optimization – Suggests code improvements for better efficiency.
🔹 Multi-Language Support – Supports Python, JavaScript, C++, and Java.
🔹 AI-Powered Explanation – Provides clear, human-readable explanations for fixes.
🔹 Code Quality Grading – AI scores your code based on efficiency and best practices.
🔹 Syntax Highlighting – Ensures properly formatted, easy-to-read code.
🔹 Downloadable Fixed Code – Allows users to save AI-generated code fixes.
🔹 Secure API Key Handling – Uses environment variables for safe authentication.

🛠 Installation

1️⃣ Install Required Dependencies

Run the following command to install the necessary libraries:

pip install streamlit groq pygments

2️⃣ Set Up Your API Key

FixGenie uses Groq’s mixtral-8x7b-32768 model. Set your API key securely:

On macOS/Linux:

export GROQ_API_KEY="your-api-key-here"

On Windows (PowerShell):

$env:GROQ_API_KEY="your-api-key-here"

▶ Usage

1️⃣ Run FixGenie

Start the application using Streamlit:

streamlit run app.py

2️⃣ Input Buggy Code
	•	Select your programming language.
	•	Paste your buggy code into the input field.
	•	Click “Fix & Optimize Code”.

3️⃣ Get AI Fixes & Explanations
	•	AI fixes and optimizes your code.
	•	Provides explanations for the fixes.
	•	Gives your code a quality rating (1-10).

4️⃣ Download Fixed Code
	•	Click “Download Fixed Code” to save your AI-generated fixes.

🖥 Example Code to Test

🔹 Super Tough Python Test Code

Paste this buggy Python code into FixGenie to test AI debugging:

import collections

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] == []  # ❌ Incorrect assignment (should be `= []`)
        self.graph[u].append(v)
        self.graph[v].append(u)  # ❌ Might create issues in a directed graph

    def bfs(self, start):
        visited = set()
        queue = collections.deque(start)  # ❌ Incorrect deque initialization
        path = []

        while queue:
            node = queue.pop(0)  # ❌ Inefficient `pop(0)`, should use `popleft()`
            if node not in visited:
                visited.append(node)  # ❌ Should be `add()`
                path.append(node)
                for neighbor in self.graph[node]:
                    queue.append(neighbor)  # ❌ Possible infinite loop

        return path

✅ Check if FixGenie corrects all these issues!

🔧 Configuration

Customizing the AI Model

By default, FixGenie uses mixtral-8x7b-32768.
You can change it in app.py:

model="mixtral-8x7b-32768"

Alternatively, try:

model="llama-3.3-70b-versatile"

if Mixtral is unavailable.

🌎 Deployment Options

To share FixGenie with others, deploy it on:
	1.	Streamlit Cloud → streamlit.io/sharing
	2.	Hugging Face Spaces → huggingface.co/spaces
	3.	Render.com (for backend hosting)
	4.	AWS/GCP/Azure (for enterprise-level hosting)

🎯 Roadmap & Upcoming Features

🚀 Future Enhancements:
🔹 Integration with GitHub (Auto-scan repositories for bugs)
🔹 Live Debugging Mode (Real-time AI-assisted debugging)
🔹 Support for More Languages (Rust, Go, Kotlin, Swift)
🔹 AI-powered Code Refactoring (Not just fixing bugs, but improving overall structure)

🤝 Contributing

We welcome contributions! To contribute:
	1.	Fork this repository
	2.	Create a new branch
	3.	Submit a pull request (PR)

📜 License

This project is licensed under the MIT License.

🛠 Credits & Acknowledgments

FixGenie is powered by:
	•	Groq API
	•	mixtral-8x7b-32768 (Mixtral Model)
	•	Streamlit
	•	Python

Special thanks to all developers who make AI coding assistants a reality! 🚀

📞 Support & Contact

For issues or feedback:
	•	GitHub Issues: Submit a Bug Report
	•	Email: support@fixgenie.com
	•	Twitter: @FixGenieAI

🚀 Fix your code instantly with FixGenie – AI-powered debugging & optimization! 🪄
