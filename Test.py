# from RAG_ChatGPT import stream_sentences

# for sentence in stream_sentences("你是誰"):
#     if sentence:
#         print(sentence)

import time
from genQuestion import generate_question

while True:
    start_time = time.time()  # 開始計時
    question = generate_question()
    end_time = time.time()  # 結束計時

    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    
    if question:
        print(question)
    else:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Duration: {end_time - start_time:.6f} seconds\n")
