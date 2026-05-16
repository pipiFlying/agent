from typing_extensions import  TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from day01.tools import call_llm
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage

llm = call_llm()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 创建智能体
def agent(state: State) -> State:
    # 将用户输入的消息传递给大模型
    response = llm.invoke(state['messages'])
    return {'messages': response}

# 创建graph，并将智能体与节点绑定
builder = StateGraph(State)
builder.add_node('node_01', agent)
builder.add_edge(START, 'node_01')
builder.add_edge('node_01', END)

# 创建节点记忆对象
memory = MemorySaver()

# 编译图
graph = builder.compile(checkpointer=memory)
config = {'recursion_limit': 2, 'configurable': {'thread_id': '1', 'session_id': 'chat_01'}}


def chat(user_input: str):
    print(f'user: {user_input}')
    print('system: ', end='')
    for chunk, metadata in graph.stream(
            # {"messages": [("user", user_input)]},
            {'messages': [HumanMessage(content=user_input)]},
            config=config,
            stream_mode='messages'
    ):
        # 核心：只打印来自 node_01 的内容，且排除掉输入的消息
        if metadata.get('langgraph_node') == 'node_01':
            if chunk.content:
                print(chunk.content, end='', flush=True)
    print('\n' + '-' * 20)

chat('你好')
chat('我叫小明')
chat('我叫什么名字？')

