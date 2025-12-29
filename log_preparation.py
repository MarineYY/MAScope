import json
import uuid
import os
import sys
import uuid
from typing import Dict
from provenance_graph.event_type_config import LOG_TYPE

class PreparationLog:
    def __init__(self, host_uuid: str, event_uuid: str, event_type: str, event_timestamp: str, subject_uuid: str, subject_name: str, object_uuid: str, object_path: str, prompt: str, response: str):
        self.host_uuid = host_uuid
        self.event_uuid = event_uuid
        self.event_type = event_type
        self.event_timestamp = event_timestamp
        self.subject_uuid = subject_uuid
        self.subject_name = subject_name
        self.object_uuid = object_uuid
        self.object_path = object_path
        self.prompt = prompt
        self.response = response

    def to_dict(self) -> Dict[str, str]:
        return {
            'host_uuid': self.host_uuid,
            'event_uuid': self.event_uuid,
            'event_timestamp': self.event_timestamp,
            'event_type': self.event_type,
            'subject_uuid': self.subject_uuid,
            'subject_name': self.subject_name,
            'object_uuid': self.object_uuid,
            'object_name': self.object_path,
            'prompt': self.prompt,
            'response': self.response,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

type_dict = {
    'FileIoCreate': 'file_write',
    'FileIoFileCreate': 'file_write',
    'FileIoWrite': 'file_write',
    'FileIoRenamePath': 'file_modify',
    'FileIoRead': 'file_read',
    'FileIoDelete': 'file_delete',
    'ImageLoad': 'process_load',
    'TcpIpDisconnectIPV4': 'network_receive',
    'TcpIpConnectIPV4': 'network_send',
    'TcpIpAcceptIPV4': 'network_receive',
    'ProcessStart': 'process_start',
    'ProcessEnd': 'process_end',
}

preparation_events = []
preparation_logs = []

file_dict = dict()
process_dict = dict()
socket_dict = dict()

node_count = 0  

def get_uuid(name):
    """
    get uuid value of String name
    :param s:
    :return:
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

def save_node(log:json)->None:
    if log["logData"]["type"] == "OBJECT_FILE":
        file_dict[log["logData"]["id"]] = log["logData"]["path"]
    elif log["logData"]["type"] == "SUBJECT_PROCESS":
        process_dict[log["logData"]["id"]] = log["logData"]["processName"]
    elif log["logData"]["type"] == "OBJECT_NETFLOW":
        socket_dict[log["logData"]["id"]] = log["logData"]["dip"] + ':' + str(log["logData"]["dport"])
    else:
        print('Unknown log type: ', log["logData"]["type"])
        sys.exit(1)

    global node_count
    node_count += 1
    return

def convert_json_to_standard_format(log):
    global preparation_events
    global preparation_logs

    host_uuid = get_uuid("127.0.0.1")
    
    event_uuid = log['logData']['id']
    event_timestamp = log['logData'].get('time')
    if len(str(event_timestamp)) != 19:
        return None, None
    # 1000000000000000000
    event_type_str = log['logData']['type']

    # dict 里没有的类型就跳过
    if event_type_str not in type_dict:
        print(f"⚠️ Unknown event type: {event_type_str}, skipped")
        return None, None  # 跳过该事件

    event_type = type_dict[event_type_str]
    
    subject_uuid = log['logData']['s']
    if subject_uuid is None:
        return None, None
    object_uuid = log['logData']['d']

    if event_type in LOG_TYPE.FILE_OP:
        subject_name = process_dict.get(subject_uuid)
        if event_type == 'file_modify':
            object_uuid = log['logData']['d2']
        object_name = file_dict.get(object_uuid)

        preparation_log = PreparationLog(host_uuid, event_uuid, event_type, event_timestamp, subject_uuid, subject_name, object_uuid, object_name, "", "")

    elif event_type in LOG_TYPE.PROCESS_OP:
        subject_name = process_dict.get(subject_uuid)
        object_name = file_dict.get(object_uuid)

        preparation_log = PreparationLog(host_uuid, event_uuid, event_type, event_timestamp, subject_uuid, subject_name, object_uuid, object_name, "", "")

    elif event_type in LOG_TYPE.NET_OP:
        subject_name = process_dict.get(subject_uuid)
        object_name = socket_dict.get(object_uuid)

        preparation_log = PreparationLog(host_uuid, event_uuid, 'network_send', event_timestamp, subject_uuid, subject_name, object_uuid, object_name, "", "")
        preparation_logs.append(preparation_log.to_json())

        preparation_log = PreparationLog(host_uuid, event_uuid, 'network_receive', event_timestamp, subject_uuid, subject_name, object_uuid, object_name, "", "")

    else:
        print('Unknown event type: ', log, event_type)
        sys.exit(1)

    preparation_logs.append(preparation_log.to_json())
    return preparation_log.to_json()

if __name__ == '__main__':

    set_dict = set()
    benign_log_list = ['attack_data/provenance.jsonl']
    for index, file_path in enumerate(benign_log_list):
        print('Now processing file is ', file_path)
        if os.path.isfile(file_path): 
            with open(file_path, 'r') as f:
                for line in f:
                    data = json.loads(line)

                    if data['logType'] == "NODE":
                        save_node(data)
                    elif data['logType'] == "EVENT":
                        convert_json_to_standard_format(data)
                    else:
                        print('Unknown log type: ', data['logType'])
                        continue

            preparation_log_path = os.path.join(file_path.rsplit('/', 1)[0], f'attack.json')

            with open(preparation_log_path, 'w') as f:
                for log in preparation_logs:
                    f.write(log + '\n')

            preparation_logs = []
            file_dict = dict()
            process_dict = dict()
            socket_dict = dict()

    print('Total number of nodes: ', node_count)