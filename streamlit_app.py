import streamlit as st
import requests

# Set up the page
st.set_page_config(page_title="DocAnalyzer", layout="centered")
st.title("📘 DocAnalyzer: AI-Powered Theme Extraction from PDFs")

# ⚠️ Replace this ngrok URL with your current Colab backend URL
api_endpoint = "https://9076-34-30-235-178.ngrok-free.app/analyze"

# Upload PDF
uploaded_pdf = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_pdf:
    st.warning("⏳ Processing your document...")

    # Send file to backend
    try:
        files = {"file": uploaded_pdf.getvalue()}
        response = requests.post(api_endpoint, files=files)

        if response.status_code == 200:
            result = response.json()

            # Debug: Show raw response
            st.subheader("📦 Raw Backend Response")
            st.json(result)

            # Safe access to keys
            question = result.get("question", "❓ Question not returned.")
            summary = result.get("summary", "📝 No summary found.")
            themes = result.get("themes", "🧠 No themes extracted.")

            st.subheader("🧾 Question Asked")
            st.write(question)

            st.subheader("📖 Extracted Answer")
            st.success(summary)

            st.subheader("🧠 Identified Themes")
            st.info(themes)
        else:
            st.error(f"🚨 Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
