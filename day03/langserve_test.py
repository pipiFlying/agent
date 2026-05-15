import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from day01.tools import call_llm
from fastapi import FastAPI
from langserve import add_routes

# 加载大模型
llm = call_llm()

# 创建消息模板
template = ChatPromptTemplate([
    ('system', '将用户输入内容翻译成{language}'),
    ('human', '{content}'),
])

# 创建链式调用
chain = template | llm | StrOutputParser()

# 创建app
app = FastAPI(title='文字翻译器', description='对用户输入的文字语言进行转换。', version='1.0')

add_routes(
    app=app,
    runnable=chain,
    path='/translate',
)

if __name__ == '__main__':
    """
    postman测试接口方案：
    http://192.168.3.10:8000/translate/invoke
    参数：{"input":{"content":"我来自中国","language":"英语"},"config":{}}
    
    浏览器访问：
    http://192.168.3.10:8000/translate/playground
    
    Swagger接口文档访问
    http://192.168.3.10:8000/docs
    """
    uvicorn.run(app, host='0.0.0.0', port=8000)
