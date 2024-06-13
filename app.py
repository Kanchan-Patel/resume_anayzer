import streamlit as st
import requests
import PyPDF2 as pdf
import json
import os
#from dotenv import load_dotenv
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load environment variables from a .env file
#load_dotenv()

# Retrieve the Hugging Face API key from environment variables
#API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def get_llama_response(input, text, jd):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer [YOUR_API_KEY]"}

    payload = {
        "inputs": input.format(text=text, jd=jd, response_variable="")
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)
        parsed_response = response.json()

        if isinstance(parsed_response, list) and parsed_response:  # Check if response is a non-empty list
            generated_text = parsed_response[0].get('generated_text')  # Safely get 'generated_text'
            if generated_text is not None:
                return generated_text
            else:
                return "Generated text not found in the response."
        else:
            return "Invalid response format or empty response."

    except Exception as e:
        return f"Error: {e}"

def input_pdf_text(uploaded_file):
    """Extracts text from uploaded PDF resume."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

# Prompt Template (adjusted for flexibility)
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes.

## Instructions:
1. Read the provided job description carefully.
2. Evaluate the resume based on how well it aligns with the job requirements.
3. Provide suggestions for improvement and highlight any missing keywords or skills.
4. Print **jd match** **missingkeyboard** **profile summary** in separate line.

## Evaluation Criteria:
- **JD Match:** Percentage of how well the resume matches the job description.
- **Missing Keywords:** List of keywords or skills missing from the resume which are necessary.
- **Profile Summary:** Brief summary or assessment of the candidate's profile and what they can improve in it.

## Resume Details:
- **Resume Text:** The content of the resume will be provided for evaluation.
- **Job Description:** Paste the job description in the text area below.

**Resume:** {text}

**Job Description:** {jd}

**Output format:**

{{
 "JD Match": "{response_variable}%",
 "MissingKeywords": [],
 "Profile Summary": ""
}}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_llama_response(input_prompt, text, jd)

        st.subheader("Response from ATS:")
        st.text(response)
    else:
        st.error("Please upload a PDF file.")

# Accuracy calculation and visualization
st.title("Model Accuracy Calculator")

# Input true labels
true_labels = st.text_input("Enter true labels (comma-separated):")

# Input predicted labels
pred_labels = st.text_input("Enter predicted labels (comma-separated):")

# Calculate accuracy
def calculate_accuracy(true_labels, pred_labels):
    try:
        true_labels = [int(label.strip()) for label in true_labels.split(',')]
        pred_labels = [int(label.strip()) for label in pred_labels.split(',')]
        accuracy = accuracy_score(true_labels, pred_labels)
        return accuracy
    except Exception as e:
        return None, str(e)

# Plot accuracy
def plot_accuracy(accuracy):
    plt.figure(figsize=(5, 5))
    plt.bar(['Accuracy'], [accuracy], color='blue')
    plt.ylim(0, 1)
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy')
    plt.text(0, accuracy / 2, f'{accuracy * 100:.2f}%', ha='center', va='center', color='white', fontsize=12)
    st.pyplot(plt)

# Display accuracy
if st.button("Calculate Accuracy"):
    if true_labels and pred_labels:
        accuracy, error = calculate_accuracy(true_labels, pred_labels)
        if accuracy is not None:
            st.success(f"Accuracy: {accuracy * 100:.2f}%")
            plot_accuracy(accuracy)
        else:
            st.error(f"Invalid input. {error}")
    else:
        st.warning("Please enter both true labels and predicted labels.")
