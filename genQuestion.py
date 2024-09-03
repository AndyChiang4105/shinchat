import json
import random
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub

def random_question():
    # 讀取考點文件
    with open('q_source.txt', 'r', encoding='utf-8') as file:
        points = file.readlines()
    # 隨機選擇一個考點
    return random.choice(points).strip()
    

base_url = "https://api.chatanywhere.cn/v1"
# 向量嵌入的模型
embedding_model = OpenAIEmbeddings(base_url=base_url)
# chatLLM
llm = ChatOpenAI(model_name="gpt-4o-mini",base_url=base_url)

# 連接本地向量資料庫
chroma_db_path = "Three_Kingdoms_storage"
vectorstore = Chroma(persist_directory=chroma_db_path, embedding_function=embedding_model)

# 創建 RAG 檢索器
retriever = vectorstore.as_retriever()

# 包含RAG檢索內容的 prompt
retrieval_qa_chat_prompt = hub.pull("shinchat/kongming_qa")

combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt
)

rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

chain = rag_chain.pick("answer")

def generate_question():
    try:
        # 使用LLM生成問題
        response = chain.invoke({'input':random_question()}) 
        
        # 解析JSON
        data = json.loads(response)

        # 確保生成的JSON格式正確，包含所有必要的字段
        required_fields = ["question", "options", "answer", "explanation"]
        options_required_fields = ["option", "text"]
        
        # 檢查是否缺少主字段
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # 檢查選項格式
        for option in data["options"]:
            for field in options_required_fields:
                if field not in option:
                    raise ValueError(f"Missing required option field: {field}")
    
        return data
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")
        print("重新生成問題")

        return None

