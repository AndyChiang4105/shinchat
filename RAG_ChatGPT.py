from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub

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
retrieval_qa_chat_prompt = hub.pull("kongming_prompt")

combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt
)

rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

chain = rag_chain.pick("answer")

# 偵測句子結束
def is_end_of_sentence(chunk):
    return any(punct in chunk for punct in ['。', '！', '？'])

# 使用流式回調處理程序
def stream_sentences(input_text):
    buffer = []
    for chunk in chain.stream({"input": input_text}):
        buffer.append(chunk)
        if is_end_of_sentence(chunk):
            sentence = ''.join(buffer)
            buffer = []
            yield sentence

    # 確保輸出最後的部分
    if buffer:
        sentence = ''.join(buffer)
        yield sentence