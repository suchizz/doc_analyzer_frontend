import streamlit as st
import requests

st.set_page_config(page_title="DocAnalyzer", layout="centered")
st.title("📘 DocAnalyzer: AI-Powered Theme Extraction from PDFs")

api_endpoint = "https://8aa5-34-19-97-170.ngrok-free.app/analyze"  # Replace this

uploaded_pdf = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_pdf:
    st.warning("⏳ Uploading and analyzing document...")

    try:
        files = {
            "file": ("uploaded.pdf", uploaded_pdf.getvalue(), "application/pdf")
        }
        response = requests.post(api_endpoint, files=files)

        try:
            result = response.json()
        except Exception as e:
            st.error("🚨 Backend returned an invalid response.")
            st.code(response.text)
            st.stop()

        # Show raw backend result
        st.subheader("📦 Raw Backend Response")
        st.json(result)

        # Access keys safely
        question = result.get("question", "No question found.")
        summary = result.get("summary", "No summary found.")
        themes = result.get("themes", "No themes found.")

        st.subheader("🧾 Question Asked")
        st.write(question)

        st.subheader("📖 Extracted Answer")
        st.success(summary)

        st.subheader("🧠 Identified Themes")
        st.info(themes)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
