from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

def create_deepseek_agent(name, api_key):
    model_info = {
        "name": "deepseek-chat",
        "parameters": {"max_tokens": 2048, "temperature": 0.4, "top_p": 0.9},
        "family": "gpt-4o",
        "vision": False,
        "json_output": True,
        "function_calling": True
    }

    client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        api_key=api_key,
        model_info=model_info
    )

    agent = AssistantAgent(name=name, model_client=client)
    return agent
