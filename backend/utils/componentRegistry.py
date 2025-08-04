
from typing import Dict, Optional
from backend.tools import form_tools
from backend.utils.defineComponents import ComponentTool, RealComponentTool, defineComponentTool


class ComponentRegistry:
    _instance = None
    _components: Dict[str, RealComponentTool] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register_component(cls, name: str, config: ComponentTool):
        cls._components[name] = defineComponentTool(config)

    @classmethod
    def get_component(cls, name: str) -> Optional[RealComponentTool]:
        return cls._components.get(name)

    @classmethod
    def get_all_components(cls) -> Dict[str, RealComponentTool]:
        return cls._components

