class LOG_TYPE:
        Agent_OP = ['agent send', 'agent receive']
        Data_OP = ['data read', 'data write']
        Code_OP = ['code read', 'code write']
        Process_OP = ['process fork', 'process execute']
        Net_OP = ['network send', 'network receive']

class EVENT_TYPE:
        Event_OP = ['agent send', 'agent receive',
                    'data read', 'data write',
                    'code read', 'code write',
                    'process fork', 'process execute',
                    'network send', 'network receive']