from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings




#Extract Data from the PDF files
def load_pdf_file(data):
    loader=DirectoryLoader(path=data,loader_cls=PyPDFLoader,glob="*.pdf")
    documents=loader.load()
    return documents

#Spilt data into chunks
def split_text(documents):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    texts=text_splitter.split_documents(documents)
    return texts

#Download the embeddings from huggingface
def download_hugging_face_embedding():
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings