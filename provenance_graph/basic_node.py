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
    permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"agent_name": self.agent_name})
        # props.update({"Permission": self.Permission})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.agent_name, self.Permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.agent_name} {self.permission}"
    
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
    data_path: str = ""
    permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"data_path": self.data_path})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.data_path, self.permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.data_path} {self.permission}"
    
    def get_node_name(self):
        return self.data_path
    
    def get_node_type(self):
        return "data"
    
    def get_node_permission(self):
        return self.permission

    def set_node_permission(self, permission):
        self.permission = permission

@dataclass
class CodeNode(BasicNode):
    node_uuid: Optional[str] = None
    code_path: str = ""
    permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"Code_path": self.Code_path})
        # props.update({"Permission": self.Permission})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.code_path, self.permission)
    
    def __str__(self):
        return f"{self.node_uuid} {self.code_path} {self.permission}"
    
    def get_node_name(self):
        return self.code_path
    
    def get_node_type(self):
        return "code"

    def get_node_permission(self):
        return self.permission

    def set_node_permission(self, permission):
        self.Permission = permission

@dataclass
class ProcessNode(BasicNode):
    node_uuid: Optional[str] = None
    process_name: str = ""
    permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"process_name": self.process_name})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.process_name)
    
    def __str__(self):
        return f"Process {self.node_uuid} {self.process_name} {self.permission}"
    
    def get_node_name(self):
        return self.process_name
    
    def get_node_type(self):
        return "Process"
    
    def get_node_permission(self):
        return self.permission
    
    def set_node_permission(self, permission):
        self.permission = permission


@dataclass
class NetworkNode(BasicNode):
    node_uuid: Optional[str] = None
    ip_address: str = ""
    permission: int = 0

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"ip_address": self.ip_address})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.ip_address, self.permission)
    
    def __str__(self):
        return f"Network Connect {self.node_uuid} {self.ip_address} {self.permission}"
    
    def get_node_name(self):
        return self.ip_address.split(" : ")[0]
    
    def get_node_type(self):
        return "Network"
    
    def get_node_permission(self):
        return self.permission
    
    def set_node_permission(self, permission):
        self.permission = permission
    

