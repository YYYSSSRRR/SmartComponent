import json
from typing import Dict, Any, List
from dataclasses import dataclass
from backend.utils.componentRegistry import ComponentRegistry

@dataclass
class Action:
    component: str
    tool: str
    parameters: Dict[str, Any]

@dataclass
class LLMResponse:
    actions: List[Action]
    message: str

class LLMService:
    def __init__(self, registry:ComponentRegistry):
        self.registry = registry
    
    async def generate_tool_schema_for_llm(self) -> Dict[str, Any]:
        components = self.registry.get_all_components()
        schema = {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "component": {
                                "type": "string",
                                "enum": list(components.keys())
                            },
                            "tool": {
                                "type": "string",
                                # 动态生成每个组件可用的工具
                                "enum": []
                            },
                            "parameters": {
                                "type": "object"
                            }
                        },
                        "required": ["component", "tool", "parameters"]
                    }
                },
                "message": {"type": "string"}
            }
        }
        
        # 为每个组件添加工具描述
        component_descriptions:Dict = {}
        for comp_name, component in components.items():
            component_descriptions[comp_name] = {
                "description": component.description,
                "tools": {
                    tool_name: {
                        "description": tool_config.description, 
                        "parameters": tool_config.paramSchema.schema()
                    }
                    for tool_name, tool_config in component.tools.items()
                }
            }
        
        return {
            "schema": schema,
            "component_descriptions": component_descriptions
        }
    
    async def create_llm_prompt(self, user_input: str) -> str:
        """创建给LLM的提示"""
        tool_info = await self.generate_tool_schema_for_llm()
        
        prompt = f"""
你是一个智能助手，可以操作以下组件工具。根据用户请求，决定需要调用哪些工具。

可用组件:
"""
        for comp_name, comp_info in tool_info["component_descriptions"].items():
            prompt += f"\n- {comp_name}: {comp_info['description']}"
            for tool_name, tool_info in comp_info["tools"].items():
                prompt += f"\n  - {tool_name}: 参数schema: {json.dumps(tool_info['parameters'], indent=2)}"
        
        prompt += f"""

用户请求: {user_input}

请以JSON格式响应，包含一个"actions"数组，每个元素指定要调用的组件、工具和参数。
示例响应:
{{
    "actions": [
        {{
            "component": "Form",
            "tool": "setFormValue",
            "parameters": {{"name": "username"}}
        }}
    ],
    "message": "已设置用户名字段"
}}
"""
        return prompt
    
    async def process_llm_response(self, response: str) -> LLMResponse:
        """处理LLM的响应"""
        try:
            data = json.loads(response)
            actions = [Action(**action_dict) for action_dict in data.get("actions", [])]
            message = data.get("message", "")
            return LLMResponse(actions=actions, message=message)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise ValueError(f"无效的LLM响应: {str(e)}")
    
    async def execute_actions(self, instance: Any, response: LLMResponse) -> Dict[str, Any]:
        """执行LLM返回的操作"""
        results = []
        for action in response.actions:
            component = self.registry.get_component(action.component)
            if not component:
                results.append({
                    "component": action.component,
                    "status": "error",
                    "message": "组件不存在"
                })
                continue
            
            # 检查工具是否存在
            if action.tool not in component.tools:
                results.append({
                    "component": action.component,
                    "tool": action.tool,
                    "status": "error",
                    "message": "工具不存在"
                })
                continue
            
            # 执行工具
            try:
                result = await component.cb(instance, {action.tool: action.parameters})
                results.append({
                    "component": action.component,
                    "tool": action.tool,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "component": action.component,
                    "tool": action.tool,
                    "status": "error",
                    "message": str(e)
                })
        
        return {
            "results": results,
            "llm_message": response.message
        }