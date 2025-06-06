import streamlit as st
import requests

st.set_page_config(page_title="DocAnalyzer", layout="centered")

st.title("📘 DocAnalyzer: Chat with Your Documents")
st.markdown("Upload a PDF and get AI-powered insights with key themes.")

# 🔁 Update this URL each time Colab restarts
api_endpoint = "https://9076-34-30-235-178.ngrok-free.app/analyze"

uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_pdf:
    st.warning("Processing your document, please wait...")

    files = {"file": uploaded_pdf.getvalue()}
    response = requests.post(api_endpoint, files=files)

    
    if response.status_code == 200:
    result = response.json()
    
    # 👇 Show raw response to debug
    st.subheader("📦 Raw Response (for debugging)")
    st.json(result)

    # ✅ Use `.get()` to avoid key errors
    question = result.get("question", "No question returned")
    summary = result.get("summary", "No summary available")
    themes = result.get("themes", "No themes extracted")

    st.subheader("🧾 Question Asked")
    st.write(question)

    st.subheader("📖 Extracted Answer")
    st.success(summary)

    st.subheader("🧠 Identified Themes")
    st.info(themes)
else:
    st.error("Something went wrong. Please try again.")


