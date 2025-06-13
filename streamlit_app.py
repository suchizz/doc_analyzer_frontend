import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="📄 Doc Analyzer", layout="centered")

st.title("📄 Document Analyzer")

uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)
question = st.text_input("💬 Ask a question about the documents")

if st.button("🔍 Analyze"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        st.info("Sending request to backend...")

        # Prepare files
        files = []
        for file in uploaded_files:
            file_bytes = file.read()
            files.append(("files", (file.name, file_bytes, "application/pdf")))

        # Form field
        data = {"question": question}

        # Send POST request
        try:
            res = requests.post("https://9c33-35-232-144-248.ngrok-free.app/analyze", files=files, data=data)
            st.success(f"✅ Response received: {res.status_code}")

            try:
                result = res.json()
            except:
                st.error("❌ Failed to parse response JSON")
                st.code(res.text)
                st.stop()

            st.subheader("🧾 Question Asked")
            st.write(result.get("question", "—"))

            st.subheader("💬 Direct Answers")
            for ans in result.get("direct_answers", []):
                st.markdown(ans)

            st.subheader("📊 Document Table")
            docs = result.get("documents", [])
            if docs:
                df = pd.DataFrame(docs)
                df.rename(columns={
                    "document": "Document",
                    "page": "Page",
                    "paragraph": "Paragraph",
                    "sentence": "Sentence",
                    "answer": "Extracted Answer"
                }, inplace=True)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No matching content found.")

            st.subheader("🧠 Synthesized Theme Summary")
            st.info(result.get("theme_summary", "No theme summary available."))

        except Exception as e:
            st.error(f"Request failed: {e}")


