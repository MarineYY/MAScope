import math
import sys
import uuid
import json
from provenance_graph.event_type_config import EVENT_TYPE, LOG_TYPE
from anomaly_detection.policy_agent import PolicyAgent
from anomaly_detection.ner_agent import NERAgent

class AnomalyTagCache:
    MAX_PROPAGATION_DISTANCE = 15
    def __init__(self, event=None):
        self.uuid = uuid.uuid4() 
        if event.get_source_node_name() == 'User':
            self.user_intent = event.get_subject_context()
        else:
            self.user_intent = None
        self.history = []
        self.event_cache = []
        self.propagation_distance = 1
        self.timestamp = event.timestamp if event else None
        self.policy_agent = PolicyAgent()
        self.ner_agent = NERAgent()
        self.alert_type = None
        self.accessed_agent_info = False
        self.sensitive_entities_number = 0
    
    def propagate(self, event=None):
        new_tag = AnomalyTagCache(event)
        new_tag.user_intent = self.user_intent

        if event.get_relationship() in LOG_TYPE.AGENT_OP:
            new_tag.accessed_agent_info = True or self.accessed_agent_info
            prompt = f"""事件：{event}\n 交互内容：{event.get_subject_context()}"""
            ner_result = self.ner_agent.NER_identification(prompt)
            new_tag.history = self.history + [f"[{event.source_node.get_node_type()}: {event.source_node.get_node_name()}] - {event.get_relationship()} -> [{event.sink_node.get_node_type()}: {event.sink_node.get_node_name()}]; interaction sensitive entity: {ner_result}"]
            new_tag.sensitive_entities_number = len(json.loads(ner_result).get('entities', [])) + self.sensitive_entities_number
            print(event.get_subject_context())
            print(ner_result)
        else:
            new_tag.accessed_agent_info = self.accessed_agent_info
            new_tag.history = self.history + [f"[{event.source_node.get_node_type()}: {event.source_node.get_node_name()}] - {event.get_relationship()} -> [{event.sink_node.get_node_type()}: {event.sink_node.get_node_name()}]"]

        # 传播距离增加
        new_tag.propagation_distance = self.propagation_distance + 1
        new_tag.event_cache = self.event_cache + [event]
        
        return new_tag 
    
    def should_trigger_alert(self, event) -> bool:
        if self.accessed_agent_info:
            print(f"{event.get_relationship()}, accessed_agent_info: {self.accessed_agent_info}")
        if event.get_relationship() in EVENT_TYPE.Alert_TRIGGER_RELATIONSHIP and self.accessed_agent_info: 
            content = self.user_intent + "\n" + "\n".join(self.history)
            print(content)
            print('-'*50)
            result = self.policy_agent.Policy_Enforcement(content)
            print(result)
            return json.loads(result)['result'] == 'Yes'     
        return False
    

    def merge(self, old_tag: 'AnomalyTagCache') -> 'AnomalyTagCache':
        self.history = list(set(self.history + old_tag.history))
        self.event_cache = list(set(self.event_cache + old_tag.event_cache))
        self.accessed_agent_info = self.accessed_agent_info or old_tag.accessed_agent_info
        if old_tag.propagation_distance < self.propagation_distance:
            self.propagation_distance = old_tag.propagation_distance
        return self

    def should_attenuated(self) -> bool:
        return self.propagation_distance > AnomalyTagCache.MAX_PROPAGATION_DISTANCE
    
    def trigger_alert(self):
        return self
    
    def should_replace_tag(self, sink_tag) -> bool:
        if sink_tag.sensitive_entities_number <= self.sensitive_entities_number:
            return True
        return False

