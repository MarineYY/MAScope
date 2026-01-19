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

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"agent_name": self.agent_name})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.agent_name)
    
    def __str__(self):
        return f"uuid:{self.node_uuid}, agent:{self.agent_name}"
    
    def get_node_name(self):
        return self.agent_name
    
    def get_node_type(self):
        return "agent"

@dataclass
class FileNode(BasicNode):
    node_uuid: Optional[str] = None
    File_path: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"File_path": self.File_path})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.File_path)
    
    def __str__(self):
        return f"uuid:{self.node_uuid}, File_path:{self.File_path}"
    
    def get_node_name(self):
        return self.File_path
    
    def get_node_type(self):
        return "file"


@dataclass
class ProcessNode(BasicNode):
    node_uuid: Optional[str] = None
    process_name: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"process_name": self.process_name})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.process_name)
    
    def __str__(self):
        return f"uuid:{self.node_uuid}, process:{self.process_name}"
    
    def get_node_name(self):
        return self.process_name
    
    def get_node_type(self):
        return "process"
    
@dataclass
class NetworkNode(BasicNode):
    node_uuid: Optional[str] = None
    ip_address: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"ip_address": self.ip_address})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.ip_address)
    
    def __str__(self):
        return f"uuid:{self.node_uuid}, ip_address:{self.ip_address}"
    
    def get_node_name(self):
        return self.ip_address.split(" : ")[0]
    
    def get_node_type(self):
        return "Network"

# @dataclass
# class DataNode(BasicNode):
#     node_uuid: Optional[str] = None
#     data_path: str = ""

#     def get_properties(self) -> Dict:
#         props = super().get_properties()
#         props.update({"uuid": self.node_uuid})
#         props.update({"data_path": self.data_path})
#         return props
    
#     def copy_node_generalize(self):
#         return self.__class__(self.node_uuid, self.data_path)
    
#     def __str__(self):
#         return f"[uuid:{self.node_uuid}, data_path:{self.data_path}]"
    
#     def get_node_name(self):
#         return self.data_path
    
#     def get_node_type(self):
#         return "data"
    

# @dataclass
# class CodeNode(BasicNode):
#     node_uuid: Optional[str] = None
#     code_path: str = ""

#     def get_properties(self) -> Dict:
#         props = super().get_properties()
#         props.update({"uuid": self.node_uuid})
#         props.update({"Code_path": self.code_path})
#         # props.update({"Permission": self.Permission})
#         return props
    
#     def copy_node_generalize(self):
#         return self.__class__(self.node_uuid, self.code_path, self.permission)
    
#     def __str__(self):
#         return f"{self.node_uuid} {self.code_path} {self.permission}"
    
#     def get_node_name(self):
#         return self.code_path
    
#     def get_node_type(self):
#         return "code"
    
    