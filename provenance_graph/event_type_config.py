class LOG_TYPE:
        AGENT_OP = ['agent_invoke', 'agent_respond']
        FILE_OP = ['file_read', 'file_write', 'file_delete', 'file_modify', 'process_load']
        PROCESS_OP = ['process_start', 'process_end']
        NET_OP = ['network_send', 'network_receive']

class EVENT_TYPE:
        EVENT_OP = ['agent_invoke', 'agent_respond', 'file_read', 'file_write', 'file_delete', 'file_modify', 'process_load', 'process_start', 'process_end', 'network_send', 'network_receive']
        Alert_TRIGER_RELATIONSHIP = ['file_write', 'file_delete', 'file_modify', 'network_send']