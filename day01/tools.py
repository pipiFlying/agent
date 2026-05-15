from langchain_openai import ChatOpenAI

API_KEY = 'sk-884fc943c8504efeba0d66a99eb9d2b2'
llm = ChatOpenAI(
    model='qwen3.5-35b-a3b',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key=API_KEY,
    streaming=True,
)

def call_llm():
    return llm

if __name__ == '__main__':
    messages = [
        ("system", "你是一个优秀的语言翻译官，需要将用户输入的文字转换成英文"),
        ("human", "我爱中国！"),
    ]
    res = call_llm().invoke(messages)
    print(res)