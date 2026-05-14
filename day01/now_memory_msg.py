from day06.tools import call_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

input_messages_key = 'content'
history_messages_key = 'history_contents'

# 创建带历史消息和占位符的提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个助手'),
    MessagesPlaceholder(variable_name=f'{history_messages_key}'),
    ('user', f'{{{input_messages_key}}}')
])

# 加载大模型
llm = call_llm()

# 创建普通的链
chain = prompt | llm | StrOutputParser()

# 创建存储历史消息的存储对象
store = {}

# 获取历史消息的函数
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]

# 新的带记忆的方法
def chat(session_id: str, input_text: str):
    # 获取/创建会话历史
    history = get_session_history(session_id)
    # 调用模型
    response = ""
    for chunk in chain.stream({
        history_messages_key: history.messages,
        input_messages_key: input_text
    }):
        print(chunk, end="", flush=True)  # 逐字输出
        response += chunk
    # 换行
    print()

    # 把对话加入历史
    history.add_user_message(input_text)
    history.add_ai_message(response)

    return response


if __name__ == '__main__':
    # 同一个 session_id 共享记忆
    session_id = "user_1001"
    # 第一轮
    chat(session_id, "我家在北京")
    print("-" * 40)
    # 第二轮（能记住上下文）
    chat(session_id, "我家在哪里？")
