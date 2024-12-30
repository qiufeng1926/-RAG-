from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from loder_save_file import *


class RAG_bot(object):
    # 加载文件
    def read_doc(self,doc_path):
        loder = LoderFile(doc_path)
        # 判断是不是表格数据
        docs = loder.read_file()
        return docs

    # 切割文档
    def doc_splitter(self,docs):
        docs = docs
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        # 把docs切分成trunks，在这里只有一个doc，因为我们只抓取了一个页面；
        documents = text_splitter.split_documents(docs)
        return documents

    # 将切割的文档转化为向量
    def vector_embedding(self,documents,embeddings):
        vector = FAISS.from_documents(documents, embeddings)
        retriever = vector.as_retriever()
        return retriever

    # 生成文本链
    def doc_embedding(self,llm,prompt):
        document_chain = create_stuff_documents_chain(llm, prompt)
        return document_chain

    # 生成检索链
    def retrieval_chain(self,retriever,document_chain):
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain




if __name__ == '__main__':
    # 加载api_key
    _ = load_dotenv(find_dotenv())
    # 创建大模型实例
    llm = ChatOpenAI()
    # 创建embedding实例
    embeddings = OpenAIEmbeddings()
    # prompt模板
    prompt = ChatPromptTemplate.from_template("""仅根据提供的上传的数据回答问题:
    
    <context>
    {context}
    </context>
    
    Question: {input}""")

    # 指定输出格式
    output = StrOutputParser()

    path = "data/基于计算机视觉的人流量检测算法研究.docx"

    # 创建RAG_bot实例
    rag = RAG_bot()
    # 加载文档
    docs = rag.read_doc(path)
    # 文档切割
    documents = rag.doc_splitter(docs)
    # 存到向量数据库
    vectors = rag.vector_embedding(documents,embeddings)
    # 生成文本链
    document_chain = rag.doc_embedding(llm,prompt)
    # 生成检索链
    retrieval_chain = rag.retrieval_chain(vectors,document_chain)

    response = retrieval_chain.invoke({"input":input()})
    print(response['answer'])

