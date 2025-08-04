from pydantic import BaseModel
from backend.utils import defineComponents

class SetFormValueSchema(BaseModel):
    name: str

class TriggerSubmitSchema(BaseModel):
    pass
async def send_ws(instance, value):
    await instance.send_json({
        "type": "setFormValue",
        "payload": value
    })

async def trigger_submit(instance, value):
    await instance.send_json({
        "type": "triggerSubmit",
        "payload": value
    })


form_tool=defineComponents.defineComponentTool(defineComponents.ComponentTool(
    name="Form",
    description="用于控制前端Form表单的工具",
    tools={
        "setFormValue":defineComponents.ToolConfig(
            description="填充表单字段",
            paramSchema=SetFormValueSchema,
            cb=send_ws
        ),
        "triggerSubmit":defineComponents.ToolConfig(
            description="切换按钮",
            paramSchema=TriggerSubmitSchema,
            cb=trigger_submit
        )
    }
))