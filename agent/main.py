import asyncio
import json
from router import Router
from assistant_agent import AssistantAgent
from code_agent import CodeAgent
from executor_agent import ExecutorAgent
from user_agent import UserAgent
from log_monitor.log_monitor import log_monitor
import sys

async def main():
    router = Router()
    api_key = "sk-3ab5215d21d14c6685d668ca4d97ef21"

    user_agent = UserAgent(router)
    assistant_agent = AssistantAgent(router, api_key)
    code_agent = CodeAgent(router, api_key)
    executor_agent = ExecutorAgent(router, api_key)

    # 注册
    router.register_agent(user_agent)
    router.register_agent(assistant_agent)
    router.register_agent(code_agent)
    router.register_agent(executor_agent)

    router.agents["UserAgent"] = user_agent
    router.agents["AssistantAgent"] = assistant_agent
    router.agents["CodeAgent"] = code_agent
    router.agents["ExecutorAgent"] = executor_agent

    # 测试输入
    file_name = "/home/yangyangwei/LLM/MAScope/data/exe_evil.json"
    with open(file_name, "r", encoding="utf-8") as f:
        data = f.read()
        data = json.loads(data)

    item = data[1]
    user_input = item["content"]
    await router.route_message("UserAgent", user_input, "AssistantAgent", item)


asyncio.run(main())
