from day01.tools import call_llm
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

# 创建一个带有记忆可运行的链
memory_history_chain = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key=input_messages_key,
    history_messages_key=history_messages_key,
)

config = {'configurable': {'session_id': 1}}

for chunk in memory_history_chain.stream({'content': '我家在北京'}, config=config):
    print(chunk, end='', flush=True)

for chunk in memory_history_chain.stream({'content': '我家在哪里？'}, config=config):
    print(chunk, end='', flush=True)
