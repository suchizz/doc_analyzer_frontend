import streamlit as st
import requests

st.set_page_config(page_title="DocAnalyzer", layout="centered")
st.title("📘 DocAnalyzer: AI-Powered Theme Extraction from PDFs")

api_endpoint = "https://e23b-34-91-197-156.ngrok-free.app//analyze"  # Replace this

uploaded_pdf = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_pdf:
    st.warning("⏳ Uploading and analyzing document...")

    try:
        files = {
            "file": ("doc.pdf", uploaded_pdf.getvalue(), "application/pdf")
        }
        response = requests.post(api_endpoint, files=files)

        st.subheader("📦 Raw Backend Response")
        st.code(response.text)  # 👈 shows backend text as-is

        try:
            result = response.json()
        except Exception:
            st.error("⚠️ Could not parse JSON. Check raw response above.")
            st.stop()

        # Show parsed values if JSON is valid
        st.write("✅ Parsed:", result)
        
    except Exception as e:
        st.error(f"🔥 Critical failure: {e}")

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
