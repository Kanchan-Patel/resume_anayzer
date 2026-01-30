**📄 Smart ATS Resume Analyzer (Streamlit App)**

A Streamlit-based web application that evaluates resumes against job descriptions using a Large Language Model (LLM) and provides ATS-style feedback. It also includes a model accuracy calculator with visualization.

**🚀 Features ✅ Resume ATS Evaluation**

• Upload resume in PDF format • Paste Job Description • 📊 JD Match percentage • 🔍 Missing keywords/skills • 📝 Profile improvement summary

**📈 Model Accuracy Tool**

• Enter true & predicted labels • 📐 Calculates accuracy using scikit-learn • 📊 Visualizes results using matplotlib

**🧰 Tech Stack**

🐍 Python 📺 Streamlit 🤖 Hugging Face Inference API (Mistral-7B-Instruct) 📄 PyPDF2 📊 scikit-learn 📉 matplotlib 🌐 requests

**📦 Installation**

pip install streamlit requests PyPDF2 scikit-learn matplotlib

**🔑 API Setup**

In the code replace:

Bearer [YOUR_API_KEY]

with your Hugging Face API Token

(Using .env variables is recommended for security.)

**▶️ Run the Application**

streamlit run app.py

(Replace app.py with your file name)

**📂 Sample Output**

📊 JD Match: 78% 🔍 Missing Keywords: Docker, AWS 📝 Profile Summary: Strong profile but needs cloud experience.

📈 Accuracy Input Format

✅ True labels example: 1,0,1,1

✅ Predicted labels example: 1,1,1,0

**🚧 Future Improvements**

✨ Structured JSON parsing 🔥 Keyword heatmap 📊 Resume comparison 📈 Dashboard UI 🧠 Local LLM inference
