import streamlit as st
import requests

# ----------------------------
# 🎨 Page Configuration
# ----------------------------
st.set_page_config(
    page_title="📘 AI Theme Identifier",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 🖼 Sidebar Branding
# ----------------------------
with st.sidebar:
    st.title("🧠 Gen-AI DocBot")
    st.markdown("Upload a PDF and get AI-powered summaries + themes.")
    st.markdown("Built for **Wasserstoff Internship Task**")
    st.caption("Made with ❤️ using Hugging Face + Streamlit")

# ----------------------------
# 🔗 Backend API (replace with your current ngrok URL)
# ----------------------------
api_endpoint = "https://e23b-34-91-197-156.ngrok-free.app/analyze"  # ← update this every time

# ----------------------------
# 📁 File Upload
# ----------------------------
st.header("📄 Upload Your PDF Document")
uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

# ----------------------------
# 🚀 On Upload: Send to Backend
# ----------------------------
if uploaded_file:
    st.info("⏳ Uploading and analyzing your document. Please wait...")

    try:
        # Format file for request
        files = {
            "file": ("document.pdf", uploaded_file.getvalue(), "application/pdf")
        }

        # Call backend API
        response = requests.post(api_endpoint, files=files)

        # Show raw response for debugging (optional)
        st.subheader("📦 Raw Response")
        st.code(response.text)

        # Parse JSON response
        try:
            result = response.json()
        except Exception:
            st.error("❌ Could not parse response from backend. Check raw response above.")
            st.stop()

        # ----------------------------
        # ✅ Display Results
        # ----------------------------
        # Display question
st.subheader("🧾 Question Asked")
st.write(result.get("question", "—"))

# Display per-document table
st.subheader("📊 Document-Level Answers")
doc_answers = result.get("documents", [])

if doc_answers:
    import pandas as pd
    df = pd.DataFrame(doc_answers)
    st.dataframe(df[["document", "page", "paragraph", "answer"]], use_container_width=True)
else:
    st.warning("No answers returned.")

# Display synthesized theme-wise answer
st.subheader("🧠 Synthesized Theme Answer")
st.info(result.get("theme_summary", "No theme identified."))

    except Exception as e:
        st.error(f"🔥 Something went wrong while contacting the backend:\n\n{e}")

