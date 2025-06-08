import streamlit as st
import requests
import pandas as pd

# ----------------------------
# 🎨 Streamlit Setup
# ----------------------------
st.set_page_config(
    page_title="📚 Gen-AI DocBot",
    layout="centered"
)

# ----------------------------
# 🔗 BACKEND URL
# ----------------------------
api_endpoint = "https://2402-34-85-229-237.ngrok-free.app/analyze"  # 🔁 Replace every ngrok session

# ----------------------------
# 🧾 Sidebar
# ----------------------------
with st.sidebar:
    st.title("📘 Gen-AI DocBot")
    st.markdown("Upload multiple documents and ask any question to extract answers & cross-document themes.")
    st.markdown("📍 Built for **Wasserstoff Gen-AI Internship Task**")
    st.markdown("---")

# ----------------------------
# 📂 Upload PDFs Section
# ----------------------------
st.header("📄 Step 1: Upload Your Documents")
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

if "docs_uploaded" not in st.session_state:
    st.session_state.docs_uploaded = False
if uploaded_files:
    st.session_state.files = uploaded_files
    st.session_state.docs_uploaded = True
    st.success("✅ Documents uploaded! Now ask your question below.")

# ----------------------------
# 💬 Ask Question Section
# ----------------------------
if st.session_state.docs_uploaded:
    st.markdown("---")
    st.header("💬 Step 2: Ask a Question")

    question = st.text_input(
        "Enter your question:",
        value="What are the key themes discussed across all documents?"
    )

    if st.button("🔍 Analyze"):
        with st.spinner("Processing your question..."):

            try:
                files = [
                    ("files", (f.name, f.getvalue(), "application/pdf"))
                    for f in st.session_state.files
                ]
                data = {"question": question}
                response = requests.post(api_endpoint, files=files, data=data)

                # Raw backend text
                st.subheader("📦 Raw Backend Response")
                st.code(response.text)

                try:
                    result = response.json()
                except Exception:
                    st.error("❌ Could not parse backend response.")
                    st.stop()

                # 🧾 Question
                st.subheader("🧾 Question Asked")
                st.write(result.get("question", "—"))

                # 📊 Per-document answers
                st.subheader("📊 Document-Level Answers")
                docs = result.get("documents", [])
                if docs:
                    df = pd.DataFrame(docs)
                    df.rename(columns={
                        "document": "Document",
                        "page": "Page",
                        "paragraph": "Paragraph",
                        "answer": "Extracted Answer"
                    }, inplace=True)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No answers returned.")

                # 🧠 Theme Summary
                st.subheader("🧠 Synthesized Theme Answer")
                st.info(result.get("theme_summary", "No themes identified."))

            except Exception as e:
                st.error(f"🚨 Error communicating with backend: {e}")

