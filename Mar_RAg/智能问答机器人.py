import streamlit as st
import os
from werkzeug.utils import secure_filename
from config import OPENAI_API_KEY
from loder_save_file import LoderFile
from Qa_chatgpt import QaChatGPT
from RAG_embedding import RAG_bot
from langchain_openai import OpenAIEmbeddings

# 初始化聊天机器人
chatbot = QaChatGPT(api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings()

# 设置页面布局
st.title('基于上传文档的智能聊天机器人')

# 确保上传目录存在
upload_dir = 'file_data'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# 创建文件上传窗口
uploaded_file = st.file_uploader("选择文件上传", type=['txt', 'pdf', 'docx', 'xml'])

# 如果文件被上传，处理文件
if uploaded_file is not None:
    filename1 = secure_filename(uploaded_file.name)
    filename = uploaded_file.name
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    processor = LoderFile(file_path)
    doc = processor.read_file()
    save_path = processor.save_file()

    st.write(f"文件已保存至：{save_path}")
    st.write("文件内容：")
    st.write(doc)

    # 调用RAG方法初始化retrieval_chain
    prompt_template = """仅根据提供的上传的数据回答问题:

        <context>
        {context}
        </context>

        Question: {input}"""
    chatbot.RAG(file_path, embeddings, prompt_template)

# 创建聊天窗口
user_input = st.text_input("在这里输入你的问题（exit或者退出则退出聊天）：", key="chat_input")

if user_input:
    if user_input.lower() in ["exit", "退出"]:
        st.write("聊天结束。")
    else:
        try:
            response = chatbot.response(user_input)
            st.write("回答：", response)
        except ValueError as e:
            st.error(str(e))