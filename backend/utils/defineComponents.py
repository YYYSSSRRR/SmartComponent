from typing import Any, Callable, Dict, TypedDict
from pydantic import BaseModel, Field


class ToolConfig(BaseModel):
    description:str
    paramSchema: Any  
    cb: Callable[[Any, Any], Any]  

class ComponentTool(BaseModel):
    #组件工具名
    name:str
    #组件具有的功能描述
    description:str
    #组件的工具集合
    tools:dict[str,ToolConfig]

class RealComponentTool(BaseModel):
    name:str
    description:str
    #每个功能都有一个schema描述
    tools:dict[str,ToolConfig]
    #汇总所有功能在一起的tool
    cb:Callable[[Any,dict[str,Any]],None]


def getParamsSchema(tools:dict[str,ToolConfig])->Any:
    return {key:tool.paramSchema for key,tool in tools.items()}

def defineComponentTool(componentMcpConfig:ComponentTool)->RealComponentTool:
    tools=componentMcpConfig.tools
    async def combineCb(instance:Any,args:dict[str,Any])->dict[str,Any]:
        if not args:
            return {"content": [{"type": "text", "text": "no tools"}]}
        results=[]
        for key,value in args.items():
            tool=tools.get(key)
            if not tool:
                results.append({"type": "text", "text": f"tool {key} not found"})
                continue
            result=await tool.cb(instance,value)
            results.append(result)
        return {"content":results}

    return RealComponentTool(
        name=componentMcpConfig.name,
        description=componentMcpConfig.description,
        tools=tools,
        cb=combineCb,
    )