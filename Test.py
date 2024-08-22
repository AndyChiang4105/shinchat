from RAG_ChatGPT import stream_sentences
for sentence in stream_sentences("關公刮骨療毒是真的嗎?"):
        if sentence:
            print(sentence)

# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings

# base_url = "https://api.chatanywhere.cn/v1"
# embedding_model = OpenAIEmbeddings(base_url=base_url)
# chroma_db_path = "Three_Kingdoms_storage"
# vectorstore = Chroma(persist_directory=chroma_db_path, embedding_function=embedding_model)

# q = '赤壁之戰'

# docs = vectorstore.similarity_search(q)
# print(len(docs))