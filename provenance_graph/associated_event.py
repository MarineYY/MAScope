import json
from multiprocessing import context
import uuid
from dataclasses import dataclass, field
from typing import Optional
from provenance_graph import basic_node

class AssociatedEvent:
    def __init__(self, source_node=None, sink_node=None, relationship=None, time_stamp=None):
        self.source_node_tag = None
        self.sink_node_tag = None
        self.source_node = source_node  # subject
        self.sink_node = sink_node  # object
        self.relationship = relationship
        self.event_uuid = None
        self.timestamp = time_stamp
        self.generalized_event = None
        self.subject_context = None
        self.object_context = None

    def copy_generalize(self):
        if self.generalized_event is not None:
            return self.generalized_event
        generalized_event = AssociatedEvent(
            self.source_node.copy_node_generalize(),
            self.sink_node.copy_node_generalize(),
            self.relationship,
            self.timestamp
        )
        self.generalized_event = generalized_event
        return generalized_event

    def get_relationship(self):
        return self.relationship

    def get_event_uuid(self):
        return self.event_uuid
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_source_uuid(self):
        return self.source_node.node_uuid

    def get_sink_uuid(self):
        return self.sink_node.node_uuid
    
    def set_relationship(self, relationship):
        self.relationship = relationship

    def set_source_node(self, source_node):
        self.source_node = source_node

    def set_sink_node(self, sink_node):
        self.sink_node = sink_node

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def set_event_uuid(self, event_uuid):
        self.event_uuid = event_uuid

    def get_soure_node_name(self):
        return self.source_node.get_node_name()
    
    def get_sink_node_name(self):
        return self.sink_node.get_node_name()

    def __str__(self):
        return f"Event: [{self.source_node}] -> {self.relationship} -> [{self.sink_node}], ts:{self.timestamp}"
    
    def preprocess_event(self):
        return f"{self.source_node.get_node_name()}, {self.relationship}, {self.sink_node.get_node_name()}"
    
    def get_subject_node_Permisson(self):
        return self.source_node.get_node_permission()
    
    def set_subject_node_Permisson(self, permission):
        self.source_node.set_node_permission(permission)
    
    def get_object_node_Permisson(self):
        return self.sink_node.get_node_permission()
    
    def set_object_node_Permisson(self, permission):
        self.sink_node.set_node_permission(permission)

    def set_subject_context(self, context):
        self.subject_context = context

    def get_subject_context(self):
        return self.subject_context

    def set_object_context(self, context):
        self.object_context = context
    
