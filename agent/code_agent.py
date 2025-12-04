import asyncio
import os
import re
from openai import OpenAI
from log_monitor.log_monitor import log_monitor

class CodeAgent:
    def __init__(self, router, api_key, code_dir="/home/yangyangwei/LLM/command/generated_code"):
        self.router = router
        self.name = "CodeAgent"
        self.code_dir = code_dir
        os.makedirs(code_dir, exist_ok=True)
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    async def receive_message(self, source, content, item=None):
        print(f"\n🧩 [CodeAgent 收到任务]: {content}")
        content = content + item.get("msg", "")
        try:
            prompt = f"生成适当的脚本完成以下任务，只输出代码：\n{content}"
            resp = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=2048
            )
            code = resp.choices[0].message.content.strip()

            # 🧹 清洗掉 Markdown 格式符号
            if code.startswith("```"):
                code = code.split("```")[1]  # 去掉首个 ```
            if code.lower().startswith("python"):
                code = code[len("python"):].strip()  # 去掉语言声明
            if code.endswith("```"):
                code = code[:-3].strip()
            # 文件名
            filename = item.get("index", "code_task")
            filepath = os.path.join(self.code_dir, f"{filename}.py")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
                
            await self.log_monitor(self.name, filepath, content, code)
            

            # msg = f'''代码已生成，文件路径：{filepath}请执行该代码''' + item.get("msg", "")
            msg = f'''代码已生成，文件路径：{filepath}请执行该代码'''
            print(f"📝 [CodeAgent 生成代码文件]: {filepath}")
            await self.router.route_message(self.name, msg, "Assistantagent", item)
        except Exception as e:
            await self.router.route_message(self.name, f"代码生成失败: {e}", "Assistantagent", item)

    async def log_monitor(self, subject, object, prompt, response):
            log_monitor.log_agent_call(
            subject_name=subject,
            object_name=object,
            event_type="code_interaction",
            prompt=prompt,
            response=response
        )
