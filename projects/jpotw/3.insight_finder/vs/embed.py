from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings    
from dotenv import load_dotenv
import os

load_dotenv()
inference_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

model_name="jhgan/ko-sbert-nli"
model_kwargs= {'device': 'cpu'}
encode_kwargs={'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size = 600,
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex = False,
)

loader = TextLoader('test.txt', encoding = 'UTF-8')
docs = loader.load_and_split(text_splitter=text_splitter)


for doc in docs:
    print(doc.page_content)
    print("")

    
db = Chroma.from_documents(
    docs,
    embedding=hf,
    persist_directory= "huggingface2"
)
