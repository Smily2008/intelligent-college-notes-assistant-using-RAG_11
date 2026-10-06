import streamlit as st
import requests

# FastAPI backend
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Intelligent College Notes Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Intelligent College Notes Assistant")
st.write("Upload your college notes and interact with them using AI.")

# Sidebar
st.sidebar.title("Menu")

option = st.sidebar.radio(
    "Choose an option",
    ["🏠 Home", "📄 Upload Notes", "🔎 Search Notes", "💬 Chat"]
)

# Home
if option == "🏠 Home":
    st.header("Welcome! 👋")
    st.write("""
    This Intelligent College Notes Assistant helps students:

    - 📄 Upload study notes
    - 🔎 Search through notes
    - 💬 Ask questions about notes
    - 🤖 Get AI-powered answers
    """)

# Upload
elif option == "📄 Upload Notes":
    st.header("📄 Upload College Notes")

    uploaded_file = st.file_uploader(
        "Choose a PDF or text file",
        type=["pdf", "txt"]
    )

    if uploaded_file is not None:
        st.success(f"Selected: {uploaded_file.name}")

        if st.button("Upload"):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files
                )

                if response.ok:
                    st.success("✅ Notes uploaded successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Upload failed: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend.")

# Search
elif option == "🔎 Search Notes":
    st.header("🔎 Search Your Notes")

    query = st.text_input("Enter your question or search term")

    if st.button("Search"):
        if query:
            try:
                response = requests.get(
                    f"{API_URL}/search",
                    params={"query": query}
                )

                if response.ok:
                    st.subheader("Search Results")
                    st.json(response.json())
                else:
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend.")

# Chat
elif option == "💬 Chat":
    st.header("💬 Ask Your Notes")

    question = st.text_area(
        "Ask a question about your college notes"
    )

    if st.button("Ask AI"):
        if question:
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": question}
                )

                if response.ok:
                    result = response.json()

                    st.subheader("🤖 AI Answer")
                    st.write(result)

                else:
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend.")