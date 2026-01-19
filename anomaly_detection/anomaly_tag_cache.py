import math
import uuid
import json
from provenance_graph.event_type_config import LOG_TYPE
from anomaly_detection.policy_agent import PolicyAgent
from anomaly_detection.ner_agent import NERAgent

class AnomalyTagCache:
    MAX_PROPAGATION_DISTANCE = 15

    def __init__(self, event=None):
        self.uuid = uuid.uuid4() 
        self.history = []
        self.event_cache = []
        self.propagation_distance = 1
        self.timestamp = event.timestamp if event else None
        self.policy_agent = PolicyAgent()
        self.ner_agent = NERAgent()
        self.alert_type = None
    
    def propagate(self, event=None):
        new_tag = AnomalyTagCache(event)
        
        if event.get_relationship() in LOG_TYPE.Agent_OP:
            prompt = f"""
                    事件：{event} 
                    提示词命令：{event.get_subject_context()}
                    """
            ner_result = self.ner_agent.NER_identification(prompt)
        else:
            ner_result = "{}"

        new_tag.history.append(f"[{event.source_node} sensitive info: {ner_result}] - {event.get_relationship()} -> ")

        # 传播距离增加
        new_tag.propagation_distance = self.propagation_distance + 1
        new_tag.event_cache = self.event_cache + [event]
        
        return new_tag 
    
    def should_trigger_alert(self, event) -> bool:
        if event.get_relationship() in LOG_TYPE.Alert_TRIGER_RELATIONSHIP: 
            content = " ".join(self.history) + f" [{self.event_cache[-1].sink_node}]"
            result = self.policy_agent.Policy_Enforcement(content)
            return result       
        return False
    
    def should_attenuated(self) -> bool:
        return self.propagation_distance > AnomalyTagCache.MAX_PROPAGATION_DISTANCE
    
    def trigger_alert(self):
        return self
    
    def should_replace_tag(self, new_tag) -> bool:
        return new_tag.Propagation_Distance <= self.propagation_distance

