from anomaly_detection.anomaly_detection import AnomalyDetector
from provenance_graph.associated_event import AssociatedEvent
from provenance_graph.event_type_config import LOG_TYPE
from provenance_graph.basic_node import AgentNode, FileNode, ProcessNode, NetworkNode
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
            event_timestamp = log['event_timestamp']
            
            subject_uuid = log['subject_uuid']
            subject_name = log['subject_name']
            object_uuid = log['object_uuid']
            object_path = log['object_name']

            event.set_timestamp(int(event_timestamp))
            event.set_relationship(event_type)
            event.set_event_uuid(event_uuid)
            event.set_subject_context(log['prompt'])
            event.set_object_context(log['response'])
            if event_type in LOG_TYPE.AGENT_OP:

                if event_type in ['agent_invoke']:
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = AgentNode(node_uuid=object_uuid, agent_name=object_path)
                elif event_type in ['agent_respond']:
                    source_node = AgentNode(node_uuid=object_uuid, agent_name=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                elif event_type in ['tool_invoke']:
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = ProcessNode(node_uuid=object_uuid, process_name=object_path)
                elif event_type in ['tool_respond']:
                    source_node = ProcessNode(node_uuid=object_uuid, process_name=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)

            elif event_type in LOG_TYPE.FILE_OP:

                if event_type in ['file_write', 'file_delete', 'file_modify']:
                    source_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
                    sink_node = FileNode(node_uuid=object_uuid, file_path=object_path)
                else:
                    source_node = FileNode(node_uuid=object_uuid, file_path=object_path)
                    sink_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
                 
            elif event_type in LOG_TYPE.PROCESS_OP:

                source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                sink_node = ProcessNode(node_uuid=object_uuid, process_name=object_path)

            elif event_type in LOG_TYPE.NET_OP:

                if event_type in ['network_send']:
                    source_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
                    sink_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
                else:
                    source_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
                    sink_node = AgentNode(node_uuid=subject_uuid, agent_name=subject_name)
            else:
                continue

            events.append(event)
            
            event.set_source_node(source_node)
            event.set_sink_node(sink_node)

        return events

    
if __name__ == "__main__":
    test_file = "/home/yangyangwei/LLM/MAScope/data/raw_data/Unexpected Code Execution (RCE)/merged_provenance.jsonl" 
    data_loader = DataLoader(test_file)
    events = data_loader.load_events()

    anomaly_detector = AnomalyDetector() 

    for event in events:
        anomaly_detector.process_events(event)
    
    print("Anomaly detection completed.")

        