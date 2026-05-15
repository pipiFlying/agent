from langchain_core.documents import Document
from day02.db import person1, person2

# 创建document对象，加载知识数据库
docs = [
    Document(page_content=person1),
    Document(page_content=person2),
]