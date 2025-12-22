from anomaly_detection.anomaly_detection import AnomalyDetector
from provenance_graph.associated_event import AssociatedEvent
from provenance_graph.event_type_config import LOG_TYPE
from provenance_graph.basic_node import AgentNode, DataNode, CodeNode, ProcessNode, NetworkNode
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
            if event_type in LOG_TYPE.Agent_OP:

                if event_type == 'agent send':
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = AgentNode(node_uuid=object_uuid, agent_name=object_path)
                elif event_type == 'agent receive':
                    source_node = AgentNode(node_uuid=object_uuid, agent_name=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)

            elif event_type in LOG_TYPE.Data_OP:

                if event_type == 'data write':
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = DataNode(node_uuid=object_uuid, data_path=object_path)
                elif event_type == 'data read':
                    source_node = DataNode(node_uuid=object_uuid, data_path=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)

            elif event_type in LOG_TYPE.Code_OP:
                
                if event_type == 'code write':
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = CodeNode(node_uuid=object_uuid, code_path=object_path)
                elif event_type == 'code read':
                    source_node = CodeNode(node_uuid=object_uuid, code_path=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                 
            elif event_type in LOG_TYPE.Process_OP:

                source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                sink_node = ProcessNode(node_uuid=object_uuid, process_name=object_path)

            elif event_type in LOG_TYPE.Net_OP:

                if event_type == 'network send':
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
                elif event_type == 'network receive':
                    source_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
            else:
                continue

            events.append(event)
            
            event.set_source_node(source_node)
            event.set_sink_node(sink_node)

        return events

    
if __name__ == "__main__":
    test_file = "/home/yangyangwei/LLM/MAScope/attack_data/data.json" 
    data_loader = DataLoader(test_file)
    events = data_loader.load_events()

    anomaly_detector = AnomalyDetector()
    anomaly_detector.load_permission_manager()  
    

    for event in events:
        print(event)

    # for event in events:
    #     anomaly_detector.process_events(event)
    
    print("Anomaly detection completed.")

        