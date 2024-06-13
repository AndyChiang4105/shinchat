import os
import re
import uuid
import glob
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from threading import Thread
from queue import Queue
from chatGPT import getGptResponse
from soVITS_api import getVitsResponse
from faster_whisper import WhisperModel

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'static/recordings/'
app.config['PROCESSED_FOLDER'] = 'static/output/'
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

tts_queue = Queue()

def split_sentences(text):
    # 拆分句子
    sentence_endings = re.compile(r'(?<=[。！？])')
    sentences = sentence_endings.split(text)
    # 去除多餘空格
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def speach_to_text(filepath):
    model_size = "large-v2"  # tiny, base, small, medium, large, large-v2, large-v3
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    audio_path = filepath  
    segments, _info = model.transcribe(audio_path, beam_size=5, initial_prompt="繁體")
    transcription_segments = [segment.text for segment in segments]
    transcription = "，".join(transcription_segments)
    return transcription

def text_to_speech(text, output_file):
    output_bytesIO = getVitsResponse(text)
    with open(output_file, "wb") as f:
        f.write(output_bytesIO.read())

def handle_tts_queue():
    while True:
        text, sid = tts_queue.get()
        unique = str(uuid.uuid4())
        output_file = os.path.join(app.config['PROCESSED_FOLDER'], f"output_{unique}.wav")
        text_to_speech(text, output_file)
        socketio.emit('tts_done', {'file': output_file}, room=sid)

# 啟動一個新執行緒來處理TTS隊列
tts_thread = Thread(target=handle_tts_queue)
tts_thread.daemon = True
tts_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # 儲存使用者語音
        recording_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(recording_file_path)

        # 語音轉文字處理 (return 純文字)
        user_input_text = speach_to_text(filepath=recording_file_path)
        print(user_input_text)

        # 取得 gpt 回應 (return 純文字)
        assistant_response = getGptResponse(user_input_text)
        print(assistant_response)

        # 拆分 gpt 回應成句子並加入TTS隊列
        sentences = split_sentences(assistant_response)

        # 暫存訊息，讓前端後續請求將 sid 傳遞過來
        session['sentences'] = sentences

        return jsonify({'status': 'upload_success'})

@app.route('/start_tts', methods=['POST'])
def start_tts():
    data = request.json
    sid = data.get('sid')

    if not sid or 'sentences' not in session:
        return jsonify({'error': 'Invalid request'}), 400

    sentences = session.pop('sentences')

    # sentences 是一個list，儲存拆分的句子
    print(sentences)

    # 每個句子依序進行 TTS 處理
    for sentence in sentences:
        if sentence:
            tts_queue.put((sentence, sid))

    return jsonify({'status': 'tts_started'})

@socketio.on('connect')
def test_connect():
    print('Client connected', request.sid)
    emit('sid', {'sid': request.sid})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

# 將指定路徑下的檔案刪除
def clear_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    # 執行程式前先將之前的結果清理掉
    clear_folder(app.config['PROCESSED_FOLDER'])
    socketio.run(app, debug=True)
