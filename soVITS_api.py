import io
import requests

# tts的API請求地址
url = "http://127.0.0.1:9880"

def getVitsResponse(assistant_response):
    params = {
        "refer_wav_path": "乃不负先帝临终之重托也.wav",
        "prompt_text": "乃不负先帝临终之重托也",
        "prompt_language": "zh",
        "text": assistant_response,
        "text_language": "zh",
        "cut_punc": "，。"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        output_bytes = io.BytesIO(response.content)
        return output_bytes