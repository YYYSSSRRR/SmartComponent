from typing import Any, Dict, List
from fastapi import Body, FastAPI, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

from pydantic import BaseModel
from backend.tools.form_tools import form_tool


from backend.llmConstant import llm_service,llm
import logging

from backend.utils.componentRegistry2 import ComponentRegistration, ComponentRegistry2
from backend.utils.llmService import Action, LLMResponse
from backend.utils.llmService2 import LLMService2

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()


@app.websocket("/ws/mcp")
async def websocket_endpoint(websocket: WebSocket):
    print("请求进入函数")
    try:
        await websocket.accept()
        print("accept执行成功")
    except Exception as e:
        print("accept执行失败")
    
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("接收到前端消息:", data)
    except Exception as e:
        clients.remove(websocket)
        print("连接错误")
        print("_________________")
        print(e)
    
@app.get("/trigger")
async def trigger_action():
    if not clients:
        return {"error":"No connected clients"}
    
    cmd={
        "triggerSubmit":{

        },
    }

    print("触发事件:", cmd)
    await broadcast(cmd)
    return {"status": "sent"}

@app.get("/test_run")
async def test_run():
    if(not clients):
        return {"error":"No clients connected"}
    user_request="请将表单中的用户名字段设置为'张三'并提交表单"
    prompt=await llm_service.create_llm_prompt(user_request)
    response_text=await llm.ainvoke(prompt)
    llm_response=await llm_service.process_llm_response(response_text.content)
    for ws in clients.copy():
        result=await llm_service.execute_actions(ws,llm_response)
        print(result)
    return {"status":"executed"}

async def broadcast(cmd: dict):
    print("进入broadcast")
    if not clients:
        print("无连接")
    tasks = []
    for ws in clients.copy():
        tasks.append(form_tool.cb(ws, cmd))
    await asyncio.gather(*tasks, return_exceptions=True)

# @app.post("/api/llm")
# async def execute_with_llm():
#     try:
#         # 生成LLM提示并获取响应
#         prompt = await llm_service.create_llm_prompt("请将表单中的用户名字段设置为'张三'并提交表单")
#         llm_raw_response = await llm.ainvoke(prompt)  
        
#         # 处理LLM响应
#         response = await llm_service.process_llm_response(llm_raw_response)
        
#         # 返回执行计划给前端
#         return {
#             "actions": [action.dict() for action in response.actions],
#             "message": response.message,
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


registry = ComponentRegistry2()
@app.post("/api/register")
def register_component(component: ComponentRegistration):
    # 将组件信息添加到注册表
    registry.register_component(component)
    print("后端注册的组件：register",registry.get_all_components())
    return {"status":"success"}

@app.post("/api/execute")
async def executeLLM(user_input:str=Body(...,embed=True)):
    llm_service2=LLMService2(registry)
    prompt=await llm_service2.create_llm_prompt(user_input)
    response_text=await llm.ainvoke(prompt)
    response=await llm_service2.process_llm_response(response_text.content)
    print(response)
    return response
    