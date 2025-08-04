import asyncio
from backend.main import registry
from backend.utils.llmService2 import LLMService2

llm_service2=LLMService2(registry)
# def main():
#     user_input="请将表单中的用户名字段设置为'张三'并提交表单"
#     result=llm_service2.generate_tool_schema_for_llm()
#     print(result)
# main()