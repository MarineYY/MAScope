
from typing import Optional
from anomaly_detection.anomaly_tag_cache import AnomalyTagCache
from provenance_graph.associated_event import AssociatedEvent
from anomaly_detection.ner_agent import NERAgent
import time
import json

class AnomalyDetector:

    init_tag_count = 0
    propogation_tag_count = 0

    def __init__(self):
        self.tags_cache_map = {}
        self.start_time = None
        self.last_print_time = time.time()
        self.permission_manager = None
        self.processed_event_count_value = None
        self.ner_agent = NERAgent()
        self.alert_path = "anomaly_alerts.txt"

    def process_events(self, associated_event: AssociatedEvent):
        if self.processed_event_count_value is None:
            print('start detecting...\n')
            self.start_time = time.time()
            self.processed_event_count_value = 0

        self.processed_event_count_value += 1

        # 更新上次打印时间
        self.last_print_time = time.time() 
        print('=' * 50)
        print(f"Processing Event Count: {self.processed_event_count_value}")
        print(f"Event Details: {associated_event}")
        print(f"The number of Cached Tags: {len(self.tags_cache_map)}")
        print(f"Initialized Tags: {AnomalyDetector.init_tag_count}")
        print(f"Propagated Tags: {AnomalyDetector.propogation_tag_count}")

        try:
            if self.is_node_tag_cached(associated_event.source_node):
                associated_event.source_node_tag = self.get_tag_cache(associated_event.source_node)
            if self.is_node_tag_cached(associated_event.sink_node):
                associated_event.sink_node_tag = self.get_tag_cache(associated_event.sink_node)

            tag = self.process_event(associated_event)
        except Exception as e:
            print(f"[AnomalyDetector] 错误: {e}")
            return

        if tag is not None:
            alert_json_string = self.alert_generation(tag)
            with open(self.alert_path, "w") as writer:
                print("!!! Anomaly Detected !!!")
                print(alert_json_string)
                writer.write(alert_json_string)

    def process_event(self, associated_event):
        self.init_tag(associated_event)
        self.propagate_tag(associated_event)
        self.degrade_tag(associated_event)
        return self.trigger_alert(associated_event)

    def init_tag(self, associated_event) -> None:
        if associated_event.source_node_tag is not None:
            return
        
        new_tag = AnomalyTagCache(associated_event)
        AnomalyDetector.init_tag_count += 1
        self.set_tag_cache(associated_event.source_node, new_tag)


    def propagate_tag(self, associated_event) -> None:
        if self.get_tag_cache(associated_event.source_node) is None:
            return
        else:
            source_tag = self.get_tag_cache(associated_event.source_node)
            prompt = associated_event.get_subject_context()
            ner_result = self.ner_agent.NER_identifcation(prompt)
            print(ner_result)
            print('-'* 50)
            new_tag = source_tag.propagate(associated_event, ner_result, self.permission_manager)
            
            AnomalyDetector.propogation_tag_count += 1
            if associated_event.sink_node_tag is None or associated_event.sink_node_tag.should_replace_tag(new_tag):
                self.set_tag_cache(associated_event.sink_node, new_tag)

    def degrade_tag(self, associated_event) -> None:
        if self.get_tag_cache(associated_event.sink_node) is None:
            return

        sink_tag = self.get_tag_cache(associated_event.sink_node)
        if sink_tag.should_attenuated():
            self.remove_tag_cache(associated_event.sink_node)
            AnomalyTagCache.attenuated_tag_count += 1

    def trigger_alert(self, associated_event) -> Optional[AnomalyTagCache]:
        if self.get_tag_cache(associated_event.sink_node) is None:
            return None

        sink_tag = self.get_tag_cache(associated_event.sink_node)
        if sink_tag.should_trigger_alert():
            return sink_tag 
        else:
            return None

    def set_tag_cache(self, node, tag):
        self.tags_cache_map[node.node_uuid] = tag

    def is_node_tag_cached(self, node):
        return node.node_uuid in self.tags_cache_map

    def get_tag_cache(self, node):
        return self.tags_cache_map.get(node.node_uuid, None)

    def remove_tag_cache(self, node):
        if node.node_uuid in self.tags_cache_map:
            del self.tags_cache_map[node.node_uuid]
    
    def alert_generation(self, tag: AnomalyTagCache) -> str:
        full_alert_json = []
        full_alert_json.append("###############Alert###############\ncurrentTime:" + str(tag.timestamp) + "\n")
        full_alert_json.append("AlertPath:\n")
        for event in tag.Event_Cache:
            full_alert_json.append(f"{event}\n")
        full_alert_json.append(f"AlertType: {tag.alert_type}\n")
        full_alert_json.append('\n')
        return ''.join(full_alert_json)

    def load_permission_manager(self):
        file_path = "anomaly_detection/permission.json"
        data = {}
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.permission_manager = data