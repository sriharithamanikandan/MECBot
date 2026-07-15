import os
import tempfile
import chromadb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.title("📄 ChatPDF — Chat with your documents")

# --- Session state ---
if "collection" not in st.session_state:
    st.session_state.collection = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def index_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name
    pages = PyPDFLoader(path).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    ).split_documents(pages)
    col = chromadb.Client().create_collection(name=f"doc_{len(chunks)}_{uploaded_file.size}")
    col.add(
        documents=[c.page_content for c in chunks],
        ids=[f"c{i}" for i in range(len(chunks))],
        metadatas=[{"page": c.metadata.get("page", 0) + 1} for c in chunks],
    )
    return col, len(chunks)


def answer_question(collection, question, top_k=4):
    res = collection.query(query_texts=[question], n_results=top_k)
    chunks = res["documents"][0]
    if not chunks:
        return "I couldn't find anything relevant in this document.", []
    pages = sorted({m["page"] for m in res["metadatas"][0]})
    context = "\n\n".join(f"[p{res['metadatas'][0][i]['page']}] {c}"
                           for i, c in enumerate(chunks))
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content":
                "Answer using ONLY the context. Cite pages like (p3). "
                "If it's not in the context, say you don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content, pages


# --- Sidebar: upload + index ---
with st.sidebar:
    st.header("Upload a PDF")
    pdf = st.file_uploader("Choose a PDF", type="pdf")
    if pdf and st.button("Index document"):
        with st.spinner("Indexing..."):
            st.session_state.collection, n = index_pdf(pdf)
            st.session_state.messages = []
        st.success(f"Indexed {n} chunks. Ask away!")

# --- Chat area ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask a question about your document..."):
    if st.session_state.collection is None:
        st.warning("Please upload and index a PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, pages = answer_question(st.session_state.collection, question)
            if pages:
                answer += f"\n\n---\n*Sources: page(s) {', '.join(map(str, pages))}*"
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})