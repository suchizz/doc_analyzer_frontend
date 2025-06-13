# ✅ Packed Streamlit App: doc_analyzer_frontend (Extra Credit Version)

import streamlit as st
import requests
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="📚 DocBot+", layout="wide")

# Sidebar filters
st.sidebar.title("📂 Document Filters")
selected_types = st.sidebar.multiselect("Document Type", ["research", "cv", "report"], default=["research", "report", "cv"])
selected_authors = st.sidebar.multiselect("Author", ["Suchetana Jana", "Esteban Aucejo", "NBER"], default=["Suchetana Jana", "NBER"])
selected_dates = st.sidebar.date_input("Date Range", [datetime.date(2020, 1, 1), datetime.date.today()])

st.title("📚 Document Analyzer + Theme Identifier")

# Upload PDFs
uploaded_files = st.file_uploader("Upload multiple PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} documents uploaded.")

    selected_files = st.multiselect("📄 Include/Exclude Documents", [f.name for f in uploaded_files], default=[f.name for f in uploaded_files])

    question = st.text_input("💬 Ask a Question:", "What are the key findings in these documents?")

    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing documents and generating answers..."):
            # Filter and prepare file upload
            filtered = [f for f in uploaded_files if f.name in selected_files]
            files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in filtered]
            data = {"question": question}

            # Send to backend
            response = requests.post("https://89b5-34-57-16-2.ngrok-free.app/analyze", files=files, data=data)

            try:
                result = response.json()
            except:
                st.error("❌ Failed to parse backend response")
                st.code(response.text)
                st.stop()

            # Output - Raw JSON
            with st.expander("📦 Raw Response"):
                st.json(result)

            # Display user question
            st.subheader("🧾 Question Asked")
            st.write(result.get("question", "—"))

            # Direct Answers
            st.subheader("💬 Direct Answers with Citations")
            for ans in result.get("direct_answers", []):
                st.markdown(ans)

            # Document-Level Table
            st.subheader("📊 Document-Level Answer Table")
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
                st.warning("No document matches found.")

            # Theme Summary
            st.subheader("🧠 Synthesized Theme Summary")
            st.markdown(result.get("theme_summary", "No theme summary available."))

            # Source Downloads
            st.subheader("📂 Download Documents")
            for file in filtered:
                st.download_button(f"⬇️ {file.name}", file.getvalue(), file.name)

else:
    st.info("📁 Upload at least one document to begin.")


