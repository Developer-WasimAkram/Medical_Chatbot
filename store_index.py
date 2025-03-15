from src.utils import load_pdf_file,split_text,download_hugging_face_embedding



extracted_data = load_pdf_file('Data/')
text_chunks = split_text(extracted_data)
embeddings = download_hugging_face_embedding()


from pinecone import Pinecone
from pinecone import ServerlessSpec
#from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import Pinecone
from dotenv import load_dotenv
import os


load_dotenv()

os.environ['PINECONE_API_KEY']=os.getenv('PINECONE_API_KEY')


extracted_data=load_pdf_file(data='Data/')
text_chunks=split_text(extracted_data)
embeddings = download_hugging_face_embedding()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"


pc.create_index(
    name=index_name,
    dimension=384, 
    metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws", 
        region="us-east-1"
    ) 
) 

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = Pinecone.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)
