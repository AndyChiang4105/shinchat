# from RAG_ChatGPT import stream_sentences

# for sentence in stream_sentences("你是誰"):
#     if sentence:
#         print(sentence)

from genQuestion import generate_question

while(1):
    question = generate_question()
    if question:
        print(question)
    else:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")