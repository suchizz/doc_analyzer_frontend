import streamlit as st
import requests
import pandas as pd

# ----------------------------
# 🎨 Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="📚 Gen-AI DocBot",
    layout="centered",
)

# ----------------------------
# 🔗 BACKEND NGROK URL
# ----------------------------
api_endpoint = "https://59f8-34-16-214-232.ngrok-free.app/analyze"  # ⛳ Replace this

# ----------------------------
# 📘 Sidebar
# ----------------------------
with st.sidebar:
    st.title("📘 Gen-AI DocBot")
    st.markdown(
        """
        Upload multiple PDF documents and ask questions to extract specific answers with document citations.
        
        Built for **Wasserstoff Gen-AI Internship Task** 🚀
        """
    )
    st.markdown("---")

# ----------------------------
# Step 1: Upload PDFs
# ----------------------------
st.header("📄 Step 1: Upload Your Documents")
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

if "docs_uploaded" not in st.session_state:
    st.session_state.docs_uploaded = False

if uploaded_files:
    st.session_state.files = uploaded_files
    st.session_state.docs_uploaded = True
    st.success("✅ Documents uploaded successfully! Now ask a question.")

# ----------------------------
# Step 2: Ask a Question
# ----------------------------
if st.session_state.docs_uploaded:
    st.markdown("---")
    st.header("💬 Step 2: Ask a Question")

    question = st.text_input(
        "Enter your question:",
        value="What are the key issues or themes discussed in these documents?"
    )

    if st.button("🔍 Analyze"):
        with st.spinner("🔎 Processing your question..."):

            try:
                # Prepare files + form data
                files = [
                    ("files", (file.name, file.getvalue(), "application/pdf"))
                    for file in st.session_state.files
                ]
                data = {"question": question}

                # Send request to FastAPI backend
                response = requests.post(api_endpoint, files=files, data=data)

                # Show raw backend response
                st.subheader("📦 Raw Backend Response")
                st.code(response.text)

                try:
                    result = response.json()
                except Exception:
                    st.error("❌ Could not parse backend response.")
                    st.stop()

                # 🧾 Question Asked
                st.subheader("🧾 Question Asked")
                st.write(result.get("question", "—"))

                # 💬 Direct Answers
                st.subheader("💬 Direct Answers with Citations")
                answers = result.get("direct_answers", [])
                if answers:
                    for ans in answers:
                        st.markdown(f"🔹 {ans}")
                else:
                    st.warning("No direct answers found.")

                # 📊 Document-Level Answer Table
                st.subheader("📊 Document-Level Answer Table")
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
                    st.warning("No relevant document answers found.")

                # 🧠 Synthesized Theme Summary
                st.subheader("🧠 Synthesized Theme Summary")
                st.info(result.get("theme_summary", "No theme available."))

            except Exception as e:
                st.error(f"🚨 Error communicating with backend:\n\n{e}")

