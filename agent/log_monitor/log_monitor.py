import logging
import json
from autogen_core import EVENT_LOGGER_NAME
import uuid
import time
from typing import Any   

class logMonitor(logging.Logger):
    def __init__(self, name: str, log_file: str, level: int = logging.INFO):
        """
        logMonitor 初始化。
        :param name: logger 的名称。
        :param log_file: 日志文件的路径。
        :param level: 日志级别。
        """
        super().__init__(name, level)
        
        handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def monitor(self):
        """监视日志文件或流（待实现）。"""
        pass

    def log_agent_call(self, subject_name: str, object_name: str, event_type: str, prompt: Any, response: Any) -> None:
        """以 JSON 格式记录 Agent 调用信息"""
        timestamp = int(time.time() * 1000)

        subject_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, subject_name)
        object_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, object_name)
        log_entry = {
            "event_uuid": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": timestamp,
            "subject": {
                "subject_uuid": str(subject_uuid),
                "subject_name": subject_name,
            },
            "object": {
                "object_uuid": str(object_uuid),
                "object_name": object_name,
            },
            "prompt": prompt,
            "response": response,
        }
       
        self.info(json.dumps(log_entry, ensure_ascii=False))

log_monitor = logMonitor(name=EVENT_LOGGER_NAME, log_file="/home/yangyangwei/LLM/command/data/data.json")