import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_ibm.chat_models import IBMChatModel
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langgraph.prebuilt import create_react_agent
from retrieval import create_retriever
from templates import advisor_template, predictor_template, generator_template
from langchain.tools.retriever import create_retriever_tool
from tools import tavily_tool
from dotenv import load_dotenv

load_dotenv()

# IBM Watson credentials
ibm_api_key = os.getenv("IBM_CLOUD_API_KEY")
ibm_url = os.getenv("IBM_CLOUD_URL")
project_id = os.getenv("IBM_PROJECT_ID")

# Initialize IBM Chat Model
chat = IBMChatModel(
    model_id="granite-2b-chat-v1",
    credentials={
        "apikey": ibm_api_key,
        "url": ibm_url
    },
    project_id=project_id,
    temperature=0.7,
    max_new_tokens=2000
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory containing legal documents
LEGAL_DOCS_DIR = "legal_data"

def load_legal_documents():
    """Load all PDF documents from the legal_data directory."""
    docs = []
    for filename in os.listdir(LEGAL_DOCS_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(LEGAL_DOCS_DIR, filename)
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                docs.append(Document(page_content=text, metadata={"source": filename}))
            except Exception as e:
                print(f"Error loading {filename}: {str(e)}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    pdf_content = text_splitter.split_documents(docs)
    return pdf_content

# Load documents once at startup
legal_documents = load_legal_documents()

def setup_retriever():
    """Setup retriever with pre-loaded documents."""
    retriever = create_retriever(legal_documents)
    retrieval_tool = create_retriever_tool(
        retriever,
        "Pdf_content_retriever",
        "Searches and returns excerpts from the set of PDF docs.",
    )
    return retriever, retrieval_tool

def setup_agents(tools):
    advisor_graph = create_react_agent(chat, tools=tools, state_modifier=advisor_template)
    predictor_graph = create_react_agent(chat, tools=tools, state_modifier=predictor_template)
    return advisor_graph, predictor_graph

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Legal Research API! Please use one of the endpoints for requests."}

@app.post("/legal-assistance/")
async def legal_assistance(
    query: str = Form(...),
    option: str = Form(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    retriever, retrieval_tool = setup_retriever()
    tools = [tavily_tool, retrieval_tool]
    advisor_graph, predictor_graph = setup_agents(tools)
    
    inputs = {"messages": [("human", query)]}
    
    if option == "Legal Advisory":
        async for chunk in advisor_graph.astream(inputs, stream_mode="values"):
            final_result = chunk
        result = final_result["messages"][-1].content
        return {"result": result}
    
    elif option == "Legal Report Generation":
        set_ret = RunnableParallel({"context": retriever, "query": RunnablePassthrough()})
        rag_chain = set_ret | generator_template | chat | StrOutputParser()
        report = rag_chain.invoke(query)
        return {"report": report}
    
    elif option == "Case Outcome Prediction":
        async for chunk in predictor_graph.astream(inputs, stream_mode="values"):
            final_prediction = chunk
        prediction = final_prediction["messages"][-1].content
        return {"prediction": prediction}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid option selected.")

@app.post("/legal-advisory/")
async def legal_advisory_endpoint(query: str = Form(...)):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    retriever, retrieval_tool = setup_retriever()
    tools = [tavily_tool, retrieval_tool]
    advisor_graph, _ = setup_agents(tools)
    
    inputs = {"messages": [("human", query)]}
    async for chunk in advisor_graph.astream(inputs, stream_mode="values"):
        final_result = chunk
    result = final_result["messages"][-1].content
    return {"result": result}

@app.post("/case-outcome-prediction/")
async def case_outcome_prediction_endpoint(query: str = Form(...)):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    retriever, retrieval_tool = setup_retriever()
    tools = [tavily_tool, retrieval_tool]
    _, predictor_graph = setup_agents(tools)
    
    inputs = {"messages": [("human", query)]}
    async for chunk in predictor_graph.astream(inputs, stream_mode="values"):
        final_prediction = chunk
    prediction = final_prediction["messages"][-1].content
    return {"prediction": prediction}

@app.post("/report-generator/")
async def report_generator_endpoint(query: str = Form(...)):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    retriever, _ = setup_retriever()
    set_ret = RunnableParallel({"context": retriever, "query": RunnablePassthrough()})
    rag_chain = set_ret | generator_template | chat | StrOutputParser()
    report = rag_chain.invoke(query)
    return {"report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)