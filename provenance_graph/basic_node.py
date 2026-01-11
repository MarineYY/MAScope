from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class BasicNode:
    def get_properties(self) -> Dict:
        return {}
    
    def copy_node_generalize(self):
        return BasicNode()

@dataclass
class AgentNode(BasicNode):
    node_uuid: Optional[str] = None
    agent_name: str = ""
    Permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"agent_name": self.agent_name})
        # props.update({"Permission": self.Permission})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.agent_name, self.Permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.agent_name} {self.Permission}"
    
    def get_node_name(self):
        return self.agent_name
    
    def get_node_type(self):
        return "agent"

    def get_node_permission(self):
        return self.Permission
    
    def set_node_permission(self, permission):
        self.Permission = permission

@dataclass
class DataNode(BasicNode):
    node_uuid: Optional[str] = None
    Data_path: str = ""
    Permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"Data_path": self.Data_path})
        # props.update({"Permission": self.Permission})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.Data_path, self.Permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.Data_path} {self.Permission}"
    
    def get_node_name(self):
        return self.Data_path
    
    def get_node_type(self):
        return "Data"
    
    def get_node_permission(self):
        return self.Permission

    def set_node_permission(self, permission):
        self.Permission = permission

@dataclass
class CodeNode(BasicNode):
    node_uuid: Optional[str] = None
    Code_path: str = ""
    Permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"Code_path": self.Code_path})
        # props.update({"Permission": self.Permission})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.Code_path, self.Permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.Code_path} {self.Permission}"
    
    def get_node_name(self):
        return self.Code_path
    
    def get_node_type(self):
        return "Code"

    def get_node_permission(self):
        return self.Permission

    def set_node_permission(self, permission):
        self.Permission = permission
