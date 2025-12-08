import math
import uuid
import json
from provenance_graph.event_type_config import LOG_TYPE

class AnomalyTagCache:
    MAX_PROPAGATION_DISTANCE = 5

    def __init__(self, event=None):
        self.uuid = uuid.uuid4() 

        self.subject_agent_permission = 0
        self.object_agent_permission = 0
        self.data_permission = {"minimum": math.inf, "maximum": -math.inf}
        self.code_permission = {"minimum": math.inf, "maximum": -math.inf}

        self.Event_Cache = []
        self.Propagation_Distance = 1
        self.timestamp = event.timestamp if event else None

        self.alert_type = None
    
    def propagate(self, event=None, ner_result=None, permission_manager=None):
        new_tag = AnomalyTagCache(event)
        
        entity = json.loads(ner_result)
            
        data_permission = entity.get("Data", {})
        
        code_permission = entity.get("Code", {})

        new_tag.subject_agent_permission = permission_manager.get(event.get_soure_node_name(), 0)
        event.set_subject_node_Permisson(new_tag.subject_agent_permission)

        # 传播权限：将当前的最小/最大权限传播给新的标签
        if event.get_relationship() in LOG_TYPE.Agent_OP:
            new_tag.object_agent_permission = permission_manager.get(event.get_sink_node_name(), 0)
            event.set_object_node_Permisson(new_tag.object_agent_permission)
            if data_permission:
                new_tag.data_permission = self.set_permission(self.data_permission.copy(), data_permission)
                event.set_object_node_Permisson(new_tag.data_permission)
            if code_permission:
                new_tag.code_permission = self.set_permission(self.code_permission.copy(), code_permission)
                event.set_object_node_Permisson(new_tag.code_permission)

        elif event.get_relationship() in LOG_TYPE.Data_OP:
            new_tag.data_permission = self.set_permission(self.data_permission.copy(), data_permission)
            event.set_object_node_Permisson(new_tag.data_permission)
        elif event.get_relationship() in LOG_TYPE.Code_OP:
            new_tag.code_permission = self.set_permission(self.code_permission.copy(), code_permission)
            event.set_object_node_Permisson(new_tag.code_permission)
        else:
            raise ValueError(f"Unknown event relationship type: {event.get_relationship()}")

        # 传播距离增加
        new_tag.Propagation_Distance = self.Propagation_Distance + 1
        new_tag.Event_Cache = self.Event_Cache + [event]
        
        return new_tag 
    
    def should_trigger_alert(self, event) -> bool:

        if event.get_relationship() in LOG_TYPE.Agent_OP:
            if (self.subject_agent_permission != 0 and 
                self.object_agent_permission != 0):
                if self.subject_agent_permission < self.object_agent_permission:
                    self.alert_type = "LowPermissionAgent_Calls_HighPermissionAgent"
                    return True
            
            if (self.subject_agent_permission != 0 and 
                self.data_permission["maximum"] != -math.inf):
                if self.subject_agent_permission < self.data_permission["maximum"]:
                    self.alert_type = "LowTrustSubject_HighConfidentialData"
                    return True
            
            if (self.data_permission["maximum"] != -math.inf and 
                self.data_permission["minimum"] != math.inf):
                if self.data_permission["maximum"] >= 2 and self.data_permission["minimum"] < 2:
                    self.alert_type = "HighConfidentialData_To_LowSecurityDomain"
                    return True

            if self.code_permission["minimum"] != math.inf and self.code_permission["minimum"] < 1:
                self.alert_type = "UntrustedCodeExecution"
                return True 
            
            if (self.subject_agent_permission != 0 and 
                self.code_permission["maximum"] != -math.inf):
                if self.subject_agent_permission < self.code_permission["maximum"]:
                    self.alert_type = "LowTrustSubject_HighTrustCode"
                    return True 
                
        elif event.get_relationship() in LOG_TYPE.Data_OP:
            if (self.subject_agent_permission != 0 and 
                self.data_permission["maximum"] != -math.inf):
                if self.subject_agent_permission < self.data_permission["maximum"]:
                    self.alert_type = "LowTrustSubject_HighConfidentialData"
                    return True
            
            if (self.data_permission["maximum"] != -math.inf and 
                self.data_permission["minimum"] != math.inf):
                if self.data_permission["maximum"] >= 2 and self.data_permission["minimum"] < 2:
                    self.alert_type = "HighConfidentialData_To_LowSecurityDomain"
                    return True
                
        elif event.get_relationship() in LOG_TYPE.Code_OP:
            if self.code_permission["minimum"] != math.inf and self.code_permission["minimum"] < 1:
                self.alert_type = "UntrustedCodeExecution"
                return True 
            
            if (self.subject_agent_permission != 0 and 
                self.code_permission["maximum"] != -math.inf):
                if self.subject_agent_permission < self.code_permission["maximum"]:
                    self.alert_type = "LowTrustSubject_HighTrustCode"
                    return True 
        else:
            return False
    
        
        return False
    
    def should_attenuated(self) -> bool:
        return self.Propagation_Distance > AnomalyTagCache.MAX_PROPAGATION_DISTANCE
    
    def trigger_alert(self):
        # 返回当前标签作为触发的告警
        return self
    
    def should_replace_tag(self, new_tag) -> bool:
        # 如果新的标签传播距离更短，则替换
        return new_tag.Propagation_Distance <= self.Propagation_Distance
    
    def set_permission(self, dict_Permission, permission):
        for key, value in permission.items():
            if value < dict_Permission["minimum"]:
                dict_Permission["minimum"] = value
            if value > dict_Permission["maximum"]:
                dict_Permission["maximum"] = value
        return dict_Permission


