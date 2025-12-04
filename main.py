from anomaly_detection.anomaly_detection import AnomalyDetector
from provenance_graph.associated_event import AssociatedEvent
from provenance_graph.event_type_config import LOG_TYPE
from provenance_graph.basic_node import AgentNode, DataNode, CodeNode
import sys
import json

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_events(self):
        data = []
        with open(self.file_path, 'r') as file:
            for line in file:
                data.append(json.loads(line.strip()))
        
        events = []
        for log in data:
            event = AssociatedEvent()
            event_uuid = log['event_uuid']
            event_type = log['event_type']
            event_type = log['event_type']
            event_timestamp = log['timestamp']
            
            subject_uuid = log['subject']['subject_uuid']
            subject_name = log['subject']['subject_name']
            object_uuid = log['object']['object_uuid']
            object_path = log['object']['object_name']

            event.set_timestamp(int(event_timestamp))
            event.set_relationship(event_type)
            event.set_event_uuid(event_uuid)
            event.set_subject_context(log['prompt'])
            event.set_object_context(log['response'])
            events.append(event)
            if event_type in LOG_TYPE.Agent_OP:
                source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                sink_node = AgentNode(node_uuid=object_uuid, agent_name=object_path)
            elif event_type in LOG_TYPE.Data_OP:
                source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                sink_node = DataNode(node_uuid=object_uuid, Data_path=object_path)
            elif event_type in LOG_TYPE.Code_OP:
                source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                sink_node = CodeNode(node_uuid=object_uuid, Code_path=object_path)
            else:
                return event
            
            event.set_source_node(source_node)
            event.set_sink_node(sink_node)

        return events

    
if __name__ == "__main__":
    test_file = "/home/yangyangwei/LLM/command/data/data.json" 
    data_loader = DataLoader(test_file)
    events = data_loader.load_events()
    for event in events:
        print(event)

    anomaly_detector = AnomalyDetector()
    anomaly_detector.load_permission_manager()  
    
    for event in events:
        anomaly_detector.process_events(event)
    
    print("Anomaly detection completed.")

        