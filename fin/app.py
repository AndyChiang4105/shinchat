

from flask import Flask
from flask import render_template
from flask import send_file

from flask_socketio import SocketIO
from pydub import AudioSegment
import io
import whisper

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/get_audio')
# def get_audio():
#     # 假設音頻檔案保存在 server 的根目錄下名為 "output.wav"
#     # Use the correct path and filename for your audio file
#     return send_file("output.wav", mimetype="audio/wav")

@socketio.on('audio_data')
def handle_audio_data(data):
    print("接收到音頻數據")

    audio_file = io.BytesIO(data)
    sound = AudioSegment.from_file(audio_file, format="webm")
    sound.export("output.wav", format="wav")
    print("音频数据已保存为 output.wav")
    model = whisper.load_model("medium")
    audio = whisper.pad_or_trim(whisper.load_audio("output.wav"))
    # print(whisper.transcribe(model, audio)['text'],language="zh")

    # 转录音频
    result = whisper.transcribe(model, audio, language='zh')
    print(result['text'])

  
   # print("前端請求獲取錄音檔案")
    return send_file("output.wav", as_attachment=False)


@app.route('/play_audio')
def play_audio():
    return send_file("output.wav", as_attachment=True)

if __name__ == '__main__':
    socketio.run(app)

