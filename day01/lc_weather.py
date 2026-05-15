from day01.tools import call_llm
from langchain_core.tools import tool
from langchain.agents import create_agent
from typing_extensions import Annotated

@tool
def get_weather(city: Annotated[str, '城市名称']):
    """
    查询城市天气
    """
    if city == '成都':
        return '天气晴朗，28℃'

llm = call_llm()

graph = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt='你是一个助手'
)

inputs = {
    'messages': [
        {'role': 'user', "content": "成都天气怎样？"}
    ]
}

for chunk in graph.stream(inputs, stream_mode="updates"):
    # print(chunk)
    if "model" in chunk:
        model_content = chunk["model"]["messages"][0].content
        print(model_content)
    elif "tools" in chunk:
        tools_content = chunk["tools"]["messages"][0].content
        print(tools_content)
