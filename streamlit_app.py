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
        st.subheader("🧾 Question Asked")
        st.write(result["question"])

        st.subheader("📖 Extracted Summary")
        st.success(result["summary"])

        st.subheader("🧠 Identified Themes")
        st.info(result["themes"])
    else:
        st.error("Something went wrong. Please try again.")
