from openai import OpenAI

client = OpenAI(
   base_url="https://api.chatanywhere.cn/v1"
)

# 讀取角色設定文件內容
with open('shin35.txt', 'r', encoding='utf-8') as file:
   system_content = file.read()

# 定義初始的 messages 列表
messages = [{
    "role": "system",
    "content": system_content
}]

# tts的API請求地址
url = "http://127.0.0.1:9880"

# 流式gpt回應
def gpt_35_api_stream(messages: list):
   response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=messages,
      stream=True,
   )
   full_response = ""
   for chunk in response:
      if chunk.choices[0].delta.content is not None:
         full_response += chunk.choices[0].delta.content

   return full_response

def getGptResponse(user_input_text):
    messages.append({
         'role': 'user',
         'content': user_input_text
    })

    # 獲取 assistant 的回應
    assistant_response = gpt_35_api_stream(messages)
    return assistant_response