import os
import tempfile
import chromadb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client()

st.set_page_config(
    page_title="📄 ChatPDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ChatPDF using Groq + ChromaDB")

if "collection" not in st.session_state:
    st.session_state.collection = None

if "messages" not in st.session_state:
    st.session_state.messages = []import os
import tempfile
import chromadb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client()

st.set_page_config(
    page_title="📄 ChatPDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ChatPDF using Groq + ChromaDB")

if "collection" not in st.session_state:
    st.session_state.collection = None

if "messages" not in st.session_state:
    st.session_state.messages = []