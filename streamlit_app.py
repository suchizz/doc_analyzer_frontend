import streamlit as st
import requests
import pandas as pd

# ----------------------------
# 🎨 Streamlit Page Settings
# ----------------------------
st.set_page_config(
    page_title="Gen-AI Theme Analyzer",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 🖼 Sidebar Branding
# ----------------------------
with st.sidebar:
    st.title("📚 Gen-AI DocBot")
    st.markdown("Upload multiple documents and extract per-document answers & cross-document themes.")
    st.caption("🚀 Wasserstoff Internship Task")
    st.markdown("---")

# ----------------------------
# 🔗 BACKEND API URL (Update this when ngrok restarts)
# ----------------------------
api_endpoint = "https://8634-34-85-229-237.ngrok-free.app/analyze"  # 🔁 Replace this with your live ngrok URL

# ----------------------------
# 📤 Upload Multiple PDFs
# ----------------------------
st.header("📄 Upload Your Documents")
uploaded_files = st.file_uploader("Select one or more PDF files", type=["pdf"], accept_multiple_files=True)

# ----------------------------
# 📥 Send to Backend & Display Results
# ----------------------------
if uploaded_files:
    st.info("⏳ Uploading and analyzing documents...")

    try:
        # Prepare files for FastAPI
        files = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]
        response = requests.post(api_endpoint, files=files)

        # 📦 Show raw backend response for debugging
        st.subheader("📦 Raw Backend Response")
        st.code(response.text)

        # ✅ Try to parse JSON response
        try:
            result = response.json()
        except Exception:
            st.error("❌ Could not parse backend response. Check raw text above.")
            st.stop()

        # ----------------------------
        # ✅ Display Results
        # ----------------------------

        # 🧾 Question Asked
        st.subheader("🧾 Question Asked")
        st.write(result.get("question", "—"))

        # 📊 Document-Level Answers Table
        st.subheader("📊 Document-Level Answers")
        doc_answers = result.get("documents", [])

        if doc_answers:
            df = pd.DataFrame(doc_answers)
            df.rename(columns={
                "document": "Document",
                "page": "Page",
                "paragraph": "Paragraph",
                "answer": "Extracted Answer"
            }, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No answers returned from any documents.")

        # 🧠 Synthesized Theme Answer
        st.subheader("🧠 Synthesized Theme Answer")
        st.info(result.get("theme_summary", "No themes identified."))

    except Exception as e:
        st.error(f"🚨 Error communicating with backend:\n\n{e}")

