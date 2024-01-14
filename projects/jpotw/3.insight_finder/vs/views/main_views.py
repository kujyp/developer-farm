from flask import Blueprint, render_template, request
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from langchain.embeddings.huggingface import HuggingFaceEmbeddings    
import os
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


#openai api key
load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key,
                    model_name="gpt-3.5-turbo", 
                    streaming=True, 
                    callbacks=[StreamingStdOutCallbackHandler()],
                    temperature=0
                 )
embeddings=HuggingFaceEmbeddings()
db=Chroma(
    persist_directory="vs/huggingface2",
    embedding_function=embeddings
)

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        question = request.form.get('question') #html에서 name="question"인 것을 가져옴

        #RetrievalQA chain 만들기
        qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff", #4가지 체인 방식중 가장 심플한
                                 return_source_documents=True, #참고문헌 표시
                                 retriever=db.as_retriever(         #db를 retriever 검색기로 이용하겠다는 뜻
                                     search_type="mmr", #다양한 소스 참고
                                     search_kwargs={'k':3, 'fetch_k':10})#fetch_k 후보군 총개수
                                 )
        result = qa(question)
        ai_answer = result['result']
        print(ai_answer)
        source_document = result['source_documents']
        print(source_document)
        resource = []
        for document in source_document:
            resource.append(document.page_content)
        print(resource)
        return render_template('answer.html', question=question, ai_answer=ai_answer, resource=resource)
    
    else:
        return render_template('main.html')