import asyncio
import os
from dotenv import load_dotenv
import openai

from backend.utils.llmService import LLMService

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=api_key
os.environ["OPENAI_API_BASE"]="https://api.chatanywhere.tech/v1"
from langchain.chat_models import init_chat_model
llm=init_chat_model("gpt-4o-mini",model_provider="openai")


# 单例实例
from backend.tools.form_tools import form_tool
from backend.utils.componentRegistry import ComponentRegistry

component_registry = ComponentRegistry()
component_registry.register_component(form_tool.name,form_tool)
llm_service=LLMService(component_registry)
prompt=""
response=""

# async def main():
#     user_request = "请将表单中的用户名字段设置为'张三'并提交表单"
#     prompt = await llm_service.create_llm_prompt(user_request)
#     response=await llm.ainvoke(prompt)
#     result=await llm_service.process_llm_response(response.content)
#     print(result)

# # 异步执行
# asyncio.run(main())

