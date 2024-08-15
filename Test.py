# from RAG_ChatGPT import stream_sentences

# for sentence in stream_sentences("你是誰"):
#     if sentence:
#         print(sentence)

# import random


# def random_question():
#     # 讀取考點文件
#     with open('q_source.txt', 'r', encoding='utf-8') as file:
#         points = file.readlines()

#     # 隨機選擇一個考點
#     return random.choice(points).strip()

# print(type(random_question))
# print(f"選擇的考點是：{selected_point}")
from genQuestion import getQuestion

while(1):
    print(getQuestion())