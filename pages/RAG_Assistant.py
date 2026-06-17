import os
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

from langchain_groq import ChatGroq

load_dotenv()

st.title("📚 Finance RAG Assistant")

pdf = st.file_uploader(
    "Upload Finance PDF",
    type=["pdf"]
)

if pdf:

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    pdf_path = os.path.join(
        "uploads",
        pdf.name
    )

    with open(pdf_path, "wb") as f:
        f.write(pdf.getbuffer())

    st.success("PDF Uploaded")

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    st.write(
        f"Pages Loaded: {len(docs)}"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        docs
    )

    st.write(
        f"Chunks Created: {len(chunks)}"
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vector_db"
    )

    st.success(
        "Vector Database Created"
    )

    question = st.text_input(
        "Ask Question From PDF"
    )

    if question:

        retriever = vector_db.as_retriever(
            search_kwargs={"k": 3}
        )

        retrieved_docs = (
            retriever.get_relevant_documents(
                question
            )
        )

        context = "\n\n".join(
            [
                doc.page_content
                for doc in retrieved_docs
            ]
        )

        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        prompt = f"""
You are a Finance Document Assistant.

Answer ONLY from the context below.

Context:
{context}

Question:
{question}

If answer not found,
say:
'Information not available in document.'
"""

        response = llm.invoke(
            prompt
        )

        st.subheader("Answer")

        st.write(
            response.content
        )

        with st.expander(
            "Retrieved Context"
        ):

            st.write(context)