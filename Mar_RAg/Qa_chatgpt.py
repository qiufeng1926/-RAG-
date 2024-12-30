from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from loguru import logger
from config import *
from RAG_embedding import *


class QaChatGPT:
    def __init__(self, api_key=OPENAI_API_KEY):
        """
        初始化
        :param api_key: 设置 OpenAI API 密钥
        """
        self.llm = ChatOpenAI(api_key=api_key)
        self.retrieval_chain = None  # 初始化retrieval_chain属性



    def promptTemplate(self, prompt_template):
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return prompt

    def RAG(self,path,embeddings,prompt_Template):
        rag = RAG_bot()
        llm = self.llm
        prompt = self.promptTemplate(prompt_Template)
        # 加载文档
        docs = rag.read_doc(path)
        # 文档切割
        documents = rag.doc_splitter(docs)
        # 存到向量数据库
        retriever = rag.vector_embedding(documents, embeddings)
        # 生成文本链
        document_chain = rag.doc_embedding(llm, prompt)
        # 生成检索链
        self.retrieval_chain = rag.retrieval_chain(retriever, document_chain)
        return self.retrieval_chain

    # def response(self, query):
    #     response = retrieval_chain.invoke({"input":query})
    #     return response['answer']

    def response(self, query):
        if self.retrieval_chain is None:
            raise ValueError("Retrieval chain is not initialized. Please run RAG method first.")
        response = self.retrieval_chain.invoke({"input": query})
        return response['answer']
    


if __name__ == "__main__":
    # 创建实例
    gpt = QaChatGPT()
    embeddings = OpenAIEmbeddings()
    # prompt模板
    prompt = ("""仅根据提供的上传的数据回答问题:

    <context>
    {context}
    </context>

    Question: {input}""")


    # 指定输出格式
    output = StrOutputParser()
    # 加载文件路径
    path = "data/基于计算机视觉的人流量检测算法研究.docx"
    # 生成检索
    retrieval_chain = gpt.RAG(path,embeddings,prompt)
    # 回应
    response = retrieval_chain.invoke({"input":input()})
    print(response['answer'])



