from flask import Flask,render_template,jsonify, request  
from src.utils import  download_hugging_face_embedding
#from langchain_pinecone import PineconeVectorStore
#from langchain.vectorstores import Pinecone
from langchain_community.vectorstores import Pinecone
from src.prompt import *
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()



#os.environ['PINECONE_API_KEY']=os.getenv('PINECONE_API_KEY')


app = Flask(__name__)

embeddings = download_hugging_face_embedding()

index_name  = "medicalbot"

docsearch = Pinecone.from_existing_index(index_name=index_name,embedding=embeddings)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm=ChatGroq(model="qwen-2.5-32b")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8888, debug= True)
