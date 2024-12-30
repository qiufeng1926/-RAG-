import os
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
load_dotenv(find_dotenv())

# 获取 OpenAI API 密钥
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
