import asyncio

class UserAgent:
    def __init__(self, router):
        self.router = router
        self.name = "UserAgent"

    async def start(self):
        while True:
            user_input = input("👤 请输入任务（或输入 exit 退出）: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            await self.router.route_message("UserAgent", user_input, target="AssistantAgent")

    async def receive_message(self, source, content, item=None):
        print(f"\n💬 [来自 {source} 的回复]: {content}\n")
