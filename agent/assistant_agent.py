import asyncio
import sys
from openai import OpenAI
from log_monitor.log_monitor import log_monitor

class AssistantAgent:
    def __init__(self, router, api_key):
        self.router = router
        self.name = "Assistantagent"
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        self.system_prompt = (
            "你是 AssistantAgent，负责任务调度。系统中有：\n"
            "- CodeAgent：生成并保存 Python 代码文件。\n"
            "- ExecutorAgent：执行指定的命令。\n"
            "- UserAgent：接收最终结果。\n"
            "请根据用户消息选择要调用的智能体。\n"
            "输出格式：[目标智能体]: 消息内容"
        )

    async def receive_message(self, source, content, item=None):
        print(f"\n📩 [Assistant 收到来自 {source} 的消息]: {content}")
        try:
            prompt = f"{self.system_prompt}\n用户消息: {content}"
            resp = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            result = resp.choices[0].message.content.strip()
            print(f"🤖 [Assistant 输出]: {result}")

            # 解析目标智能体
            if result.startswith("[") and "]" in result:
                target = result.split("]")[0][1:]
                message = result.split("]", 1)[1].strip()
            else:
                target = "UserAgent"
                message = result

            await self.log_monitor(source, target, content, result)

            await self.router.route_message(self.name, message, target, item)

        except Exception as e:
            print(f"[AssistantAgent] 错误: {e}")
            await self.router.route_message(self.name, f"助手执行出错: {e}", "UserAgent", item)
    
    async def log_monitor(self, source, target, prompt, response):
            log_monitor.log_agent_call(
            subject_name=source,
            object_name=target,
            event_type="agent_interaction",
            prompt=prompt,
            response=response
        )

