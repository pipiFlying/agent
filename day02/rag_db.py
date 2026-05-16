from langchain_core.documents import Document
from day02.db import person1, person2
from day01.tools import call_embedding, call_llm
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

# 创建document对象，加载知识数据库
docs = [
    Document(page_content=person1),
    Document(page_content=person2),
]

# 加载大模型
llm = call_llm()

# 加载向量转化模型
emb_model = call_embedding()

# 创建分词器
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# 创建文本分段
paragraphs_doc = splitter.split_documents(docs)

# 生成向量数据库
chroma_db = None
def get_vector_db():
    persist_directory = 'chroma_db'
    global chroma_db
    # 加载本地文件存储的向量库
    if chroma_db is not None:
        return chroma_db
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 3:
        # 本地有库 → 加载
        chroma_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=emb_model
        )
    else:
        # 本地没有 → 创建并持久化
        chroma_db = Chroma.from_documents(
            documents=paragraphs_doc,
            embedding=emb_model,
            persist_directory=persist_directory
        )

    return chroma_db

vector_db = get_vector_db()

# 创建提示词
prompts = """
问题: {question}
知识库: {Knowledge_base}
"""

# 创建模板
template = ChatPromptTemplate([
    ('system', '根据用户问题和知识库回答问题'),
    ('user', prompts)
])

# 创建检索器
def search_and_format(question):
    results = vector_db.similarity_search_with_score(question, k=2)
    return "\n".join([res[0].page_content for res in results])

# 创建检索器
retriever = RunnableLambda(vector_db.similarity_search_with_score).bind(K=2)

# 创建链
chain = {'question': RunnablePassthrough(), 'Knowledge_base': RunnableLambda(search_and_format)} | template | llm | StrOutputParser()

for chunk in chain.stream('陆承宇是做啥的？'):
    print(chunk, end="", flush=True)
