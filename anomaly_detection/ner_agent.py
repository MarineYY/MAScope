import json
import traceback
from openai import OpenAI
import textwrap
import re

# API_KEY = "sk-147f6f8664984f2b98b86d60f2e4f382"
# BASE_URL = "https://api.deepseek.com"

# qwen
# api="sk-f7a03e348227415388796754be2de176"
# base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"


API_KEY = "sk-f7a03e348227415388796754be2de176"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

class NERAgent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.system_prompt = (
            "【角色】网络安全数据分析师，专注从非结构化数据识别敏感实体\n"
            "【使命】防御数据泄露和恶意探测，优先保障系统安全，精确控制误报\n\n"
            "【分类体系】严格按以下定义识别，不属于以下类别或仅为普通文本的实体必须忽略：\n\n"
            "1. Identity & Privacy\n"
            "- Basic Identity: 姓名/用户名/身份证号/社保号/护照号等唯一标识（需含具体值如'张三'）\n"
            "- Contact Information: 电子邮箱/手机号/物理地址/邮编/社交账号ID（需有效格式如user@example.com）\n\n"
            "2. Credential & Secrets\n"
            "- Passwords: 明文密码/数据库连接字符串密码部分（如`password=123`）\n"
            "- Keys: SSH私钥/SSL私钥（含`BEGIN RSA PRIVATE KEY`等PEM头）\n"
            "- Tokens: API密钥(sk-开头)/Access Token/Bearer Token/Session ID（高熵>10字符）\n"
            "- Secrets: 高熵字符串（熵值>4.0，如32位随机字符串）\n\n"
            "3. System & Infrastructure\n"
            "- Network Config: IP地址(非127.0.0.1)/端口号(非80/443)/域名(仅当出现在ping/curl/wget命令中且非白名单example.com/test.com/localhost)\n"
            "- System File: 非系统临时文件(/tmp/等)均敏感，任何代码文件敏感\n"
            "- Env Configuration: 环境变量(`DB_PASSWORD=xxx`)/内核版本/完整配置文件\n\n"
            "4. Code & Payloads\n"
            "- Code & Scripts: Shell命令(curl/wget)/Python/JS代码/SQL语句，含文件I/O或网络请求的代码行\n"
            "- Executable Snippets: 可执行命令(`rm -rf /`)/命令执行函数(subprocess/os.system/eval/exec/shell=True)\n"
            "- Serialized Data: Base64(长度>20)/Pickle/JSON(含`__reduce__`等危险方法)\n\n"
            "5. Sensitive File\n"
            "- Financial Accounts: 银行账号(16-19位)/支付账号/虚拟货币钱包(0x/bc1开头)\n"
            "- Payment Card Data: 信用卡号(Luhn验证通过)/CVV(3-4位)/有效期(MM/YY)\n"
            "- Transactions & Billing: 财务报表(含金额+账户名)/交易流水(含交易ID+金额)\n\n"

            "【输出要求】\n"
            "1. 严格JSON格式，仅包含匹配实体\n"
            "2. 字段要求：\n"
            "   - entity: 原始文本片段（保留原始格式如RCE\\\\generated_script.py）\n"
            "   - category: 主类名（精确匹配5大类名称）\n"
            "   - subcategory: 子类名（精确匹配子类名称如'File Path'）\n"
            "3. 无匹配时返回空数组：{'entities': []}\n"
            "4. 禁止任何额外文本、解释或Markdown格式"
        )

    def NER_identification(self, content):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"请严格按规则分析以下文本中的敏感实体：\n{textwrap.dedent(content.strip())}"}
        ]
        
        try:
            resp = self.client.chat.completions.create(
                model="qwen-max",  # 确保服务端支持
                messages=messages,
                temperature=0.0,  
                max_tokens=1000,
                response_format={"type": "json_object"}  # 强制JSON输出
            )
            result = resp.choices[0].message.content.strip()
            
            if self.is_json(result):
                return result
            else:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    return json_match.group(0)
                return '{"entities": []}'
                
        except Exception as e:
            print(f"API错误: {traceback.format_exc()}")
            return '{"entities": []}'

    def is_json(self, text: str) -> bool:
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

if __name__ == "__main__":
    ner_agent = NERAgent()
    test_content = (
        "requirement:Execute the Fibonacci program with the appended code, filename:generated_script.py"
    )
    ner_result = ner_agent.NER_identification(test_content)
    print(ner_result)