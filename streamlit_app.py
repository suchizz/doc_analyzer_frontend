import streamlit as st
import requests
import pandas as pd

# ----------------------------
# 🎨 Page Settings
# ----------------------------
st.set_page_config(
    page_title="Gen-AI DocBot",
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
# 🔗 BACKEND API URL (Replace ngrok link when restarted)
# ----------------------------
api_endpoint = "https://2402-34-85-229-237.ngrok-free.app/analyze"  # ← Replace this

# ----------------------------
# 💬 Ask a Question
# ----------------------------
st.header("💬 Ask Your Question")
question = st.text_input(
    "Enter your question:",
    value="What are the key issues or themes discussed in these documents?"
)

# ----------------------------
# 📤 Upload Multiple PDFs
# ----------------------------
st.header("📄 Upload Your Documents")
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# ----------------------------
# 🚀 Analyze on Submit
# ----------------------------
if uploaded_files and question:
    st.info("⏳ Uploading documents and processing your question...")

    try:
        # Prepare multipart form data
        files = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]
        data = {"question": question}

        response = requests.post(api_endpoint, files=files, data=data)

        # 📦 Debug: Show raw backend output
        st.subheader("📦 Raw Backend Response")
        st.code(response.text)

        # ✅ Parse response
        try:
            result = response.json()
        except Exception:
            st.error("❌ Could not parse backend response. Check raw output above.")
            st.stop()

        # ----------------------------
        # ✅ Show Results
        # ----------------------------

        # Question
        st.subheader("🧾 Question Asked")
        st.write(result.get("question", "—"))

        # Document-level answers
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

        # Synthesized summary
        st.subheader("🧠 Synthesized Theme Answer")
        st.info(result.get("theme_summary", "No theme identified."))

    except Exception as e:
        st.error(f"🚨 Error connecting to backend:\n\n{e}")

