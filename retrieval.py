from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ibm.embeddings import IBMEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# IBM Watson credentials
ibm_api_key = os.getenv("IBM_CLOUD_API_KEY")
ibm_url = os.getenv("IBM_CLOUD_URL")
project_id = os.getenv("IBM_PROJECT_ID")

def load_and_chunk_pdfs(directory_path):
    docs = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            doc = Document(page_content=text, metadata={"source": filename})
            docs.append(doc)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    chunked_docs = text_splitter.split_documents(docs)
    return chunked_docs

def create_retriever(documents: list):
    """
    Function to create and return a retriever using IBM multilingual embeddings and InMemory VectorStore.
    """
    # Initialize IBM multilingual embeddings
    embeddings = IBMEmbeddings(
        model_id="granite-embedding-107m-multilingual",
        credentials={
            "apikey": ibm_api_key,
            "url": ibm_url
        },
        project_id=project_id,
        max_retries=5
    )

    vectorstore = InMemoryVectorStore(embedding=embeddings)
    vectorstore.add_documents(documents)

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Return top 4 most relevant chunks
    )