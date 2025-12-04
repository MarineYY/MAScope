import asyncio

class Router:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    async def route_message(self, source, content, target, item=None):
        print(f"\n📨 [Router] {source} → {target}: {content}")
        if target not in self.agents:
            print(f"[Router] 未找到目标智能体: {target}")
            return
        await self.agents[target].receive_message(source, content, item)
