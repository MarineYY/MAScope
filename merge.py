import json
import os

def merge_and_filter_logs(agent_trace_path, attack_path, output_path):
    agent_logs = []
    attack_logs = []

    # 1. 读取 agent_trace.jsonl
    if os.path.exists(agent_trace_path):
        with open(agent_trace_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    agent_logs.append(json.loads(line))
    
    if not agent_logs:
        print("Error: agent_trace.jsonl 为空或不存在")
        return

    # 获取时间戳范围 (假设时间戳字段为 event_timestamp)
    # 按照记录顺序取第一条和最后一条
    start_ts = int(agent_logs[0]['event_timestamp'])
    end_ts = int(agent_logs[-1]['event_timestamp'])
    
    # 如果记录不是按时间顺序排列的，建议使用 min/max:
    # timestamps = [int(log['event_timestamp']) for log in agent_logs]
    # start_ts, end_ts = min(timestamps), max(timestamps)

    print(f"时间戳过滤范围: {start_ts} 至 {end_ts}")

    # 2. 读取 attack.jsonl
    if os.path.exists(attack_path):
        with open(attack_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    attack_logs.append(json.loads(line))

    # 3. 合并数据并根据时间戳过滤
    combined_logs = agent_logs + attack_logs
    
    # 过滤掉不在 [start_ts, end_ts] 范围内的记录
    filtered_logs = [
        log for log in combined_logs 
        if start_ts <= int(log['event_timestamp']) <= end_ts
    ]

    # 4. 按照时间戳排序
    filtered_logs.sort(key=lambda x: int(x['event_timestamp']))

    # 5. 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        for log in filtered_logs:
            f.write(json.dumps(log) + '\n')

    print(f"✅ 合并完成！共保留 {len(filtered_logs)} 条记录。")
    print(f"结果已保存至: {output_path}")

if __name__ == '__main__':
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    agent_trace_file = os.path.join(current_dir, 'agent_trace.jsonl')
    attack_file = os.path.join(current_dir, 'attack.jsonl')
    merged_file = os.path.join(current_dir, 'merged_provenance.jsonl')

    merge_and_filter_logs(agent_trace_file, attack_file, merged_file)