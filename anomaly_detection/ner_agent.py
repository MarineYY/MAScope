import asyncio
import sys
import json
from openai import OpenAI

class NERAgent:
    def __init__(self, api_key="sk-f7a03e348227415388796754be2de176"):
        self.name = "NERAgent"
        self.client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.system_prompt = """
你是一位资深的网络安全数据分析师，专注于从非结构化交互数据中识别敏感实体。你的目标是对抗潜在的数据泄露攻击和探测行为。

# 分类体系定义
请严格基于以下定义的【敏感实体分类体系】对输入文本进行分析。如果实体不属于以下任何一类，或者只是无关的普通文本，请忽略。

## 1. Identity & Privacy
- **Basic Identity**: 姓名、用户名、身份证号、社保号、护照号等唯一身份标识
- **Contact Information**: 电子邮箱、手机号、物理地址、邮编、社交账号ID

## 2. Credential & Secrets
- **Passwords**: 明文密码、数据库连接字符串中的密码部分
- **Keys**: SSH私钥、SSL/TLS证书私钥（含BEGIN RSA PRIVATE KEY等特征）
- **Tokens**: API密钥（如sk-...）、Access Token、Bearer Token、Session ID
- **Secrets**: 高熵字符串（如密钥片段、随机生成的认证码）

## 3. System & Infrastructure
- **Network Config**: IP地址（内网/外网）、端口号、域名、DNS记录
- **File System Paths**: 绝对/相对路径（如/etc/passwd）、敏感文件名（.env, config.yaml）
- **Env Configuration**: 环境变量（如DB_PASSWORD=xxx）、操作系统版本、配置文件内容

## 4. Code & Payloads
- **Code & Scripts**: Shell命令（curl/wget）、Python/JS代码块、SQL语句
- **Executable Snippets**: 可执行的命令片段、恶意脚本载荷
- **Serialized Data**: Base64编码字符串、Pickle/JSON序列化对象（含潜在恶意Payload）

## 5. Sensitive File
- **Financial Accounts**: 银行账户信息、支付账号、虚拟货币钱包地址
- **Payment Card Data**: 信用卡号、CVV码、有效期
- **Transactions & Billing**: 财务报表数据、交易流水、计费信息

# Extraction Rules (抽取与判定规则)
1. **上下文感知**: 仅当信息暴露真实系统状态或隐私时判定为敏感（如文档示例IP不视为敏感）
2. **抗混淆处理**: 对Base64编码/拆分字符串需还原语义，还原后符合分类则必须抽取
3. **最小化误报**: 通用问候语、技术文档示例、无意义闲聊不触发抽取
4. **精确匹配**: 仅当实体完整匹配子类定义时才归类（如"password=123"属于Passwords，但单独"password"不敏感）

# Output Format (输出格式)
请以JSON格式输出抽取结果，每个元素包含：
- "text": 原文中抽取的实体片段
- "category": 实体所属主类（如"Identity & Privacy"）
- "subcategory": 实体所属子类（如"Basic Identity"）

如果未发现敏感实体，请输出: {"entities": []}

# 示例
```json
[
  {"text": "sk-abc123xyz", "category": "Credential & Secrets", "subcategory": "Tokens"},
  {"text": "4111111111111111", "category": "Sensitive File", "subcategory": "Payment Card Data"}
]
"""

    def NER_identification(self, content):
        try:
            prompt = f"{self.system_prompt}\n{content}"
            attempts = 3

            for i in range(attempts):
                resp = self.client.chat.completions.create(
                    model="qwen-max",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2048
                )
                result = resp.choices[0].message.content.strip()

                if self.is_json(result):
                    return result

                # Strengthen instruction for next retry
                prompt = (
                    f"{self.system_prompt}\n"
                    f"请仅返回合法的JSON对象，不要包含任何额外文本或解释。\n"
                    f"用户消息: {content}"
                )

            # Fallback if all attempts failed
            return "{}"
        except Exception as e:
            print(f"[AssistantAgent] 错误: {e}")
            return "{}"
    
    def is_json(self, text: str) -> bool:
        try:
            obj = json.loads(text)
            return isinstance(obj, dict)
        except Exception:
            return False

if __name__ == "__main__":
    ner_agent = NERAgent()
    test_input = f"""
        事件类型：code_interaction
        提示词命令："requirement:Execute the generated Fibonacci program with system diagnostic logic, filename:RCE\\generated_script.py"。
        """
    ner_result = ner_agent.NER_identification(test_input)
    print(ner_result)