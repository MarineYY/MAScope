import asyncio
import subprocess
import re
from openai import OpenAI
from log_monitor.log_monitor import log_monitor

class ExecutorAgent:
    def __init__(self, router, api_key):
        self.router = router
        self.name = "ExecutorAgent"
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    async def receive_message(self, source, content, item=None):
        print(f"\n🚀 [ExecutorAgent 收到执行请求]: {content}")
        try:
            # ✳️ 调用大模型生成执行命令
            prompt = f"""
            你是一个智能执行体。根据描述内容，推断应该执行的命令。
            示例1：
                描述内容：0.py
                返回内容：python 0.py
            示例2：
                描述内容：ls
                返回内容：ls

            只输出要执行的命令，不要多余解释。

            描述内容：
            {content}
            """

            resp = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            command = resp.choices[0].message.content.strip()
            print(f"🧠 大模型推断的命令: {command}")

            await self.log_monitor(self.name, command.split()[-1], content, command)

            # ✳️ 执行命令
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

            # ✳️ 把结果返回给 assistant
            await self.router.route_message(self.name, f"执行结果:\n{result}", "AssistantAgent")

        except subprocess.CalledProcessError as e:
            await self.router.route_message(self.name, f"执行失败: {e.output}", "AssistantAgent")

        except Exception as e:
            await self.router.route_message(self.name, f"执行异常: {e}", "AssistantAgent")

    async def log_monitor(self, source, target, prompt, response):
            log_monitor.log_agent_call(
            subject_name=source,
            object_name=target,
            event_type="code_interaction",
            prompt=prompt,
            response=response
        )
