from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 存入資料庫

file_path = 'baihuabeiqishu.txt'
loader = TextLoader(file_path, encoding='utf-8')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001", "\uff0e", "\u3002", ""
    ],
    chunk_size=500,
    chunk_overlap=20
)
split_docs = text_splitter.split_documents(documents)

print(len(split_docs))
# 初始化向量資料庫

embedding_model = OpenAIEmbeddings(base_url="https://api.chatanywhere.cn/v1")
persist_directory = 'Three_Kingdoms_storage'
vectorstore = Chroma.from_documents(documents=split_docs, embedding=embedding_model,persist_directory=persist_directory)
print('完成向量化')