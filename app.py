import os
import threading
import uuid
import glob
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from threading import Thread
from queue import Queue
from RAG_ChatGPT import stream_sentences
from soVITS_api import getVitsResponse
from faster_whisper import WhisperModel
from genQuestion import generate_question

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
        # 將文字與音檔傳回前端
        socketio.emit('tts_done', {'file': output_file,'text': text}, room=sid)

# 啟動一個新執行緒來處理TTS隊列
tts_thread = Thread(target=handle_tts_queue,)
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
        socketio.emit('user_input', {'text': user_input_text})

        session['user_input_text'] = user_input_text

        return jsonify({'status': 'upload_success'})

@app.route('/start_tts', methods=['POST'])
def start_tts():
    data = request.json
    sid = data.get('sid')

    if not sid or 'user_input_text' not in session:
        return jsonify({'error': 'Invalid request'}), 400

    user_input_text = session.get('user_input_text')

    # 每個句子依序進行 TTS 處理
    for sentence in stream_sentences(user_input_text):
        if sentence:
            print(sentence)
            tts_queue.put((sentence, sid))

    return jsonify({'status': 'tts_started'})

@app.route('/text_backend', methods=['POST'])
def text_backend():
    data = request.get_json()
    sid = data.get('sid')
    session['user_input_text'] = data.get('message', '')

    user_input_text = session.get('user_input_text')

    # 每個句子依序進行 TTS 處理
    for sentence in stream_sentences(user_input_text):
        if sentence:
            print(sentence)
            tts_queue.put((sentence, sid))

    
    response = {
        'status': 'success',
        'message': 'Message received',
    }
    return jsonify(response)

# 全局變量來存儲生成的題目
questions_pool = []

def generate_questions_async():
    global questions_pool
    while True:
        if len(questions_pool) < 20:
            for _ in range(20 - len(questions_pool)):
                question = generate_question()
                questions_pool.append(question)

# 提供 API 來返回題目
@app.route('/get_question', methods=['GET'])
def get_question():
    global questions_pool
    if questions_pool:
        return jsonify(questions_pool.pop(0))
    else:
        # 如果題目池空了，可以選擇動態生成或返回一個提示
        return jsonify({"error": "No more pre-generated questions. Please try again later."}), 404

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


@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/qa')
def qa():
    return render_template('qa.html')

@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    # 執行程式前先將之前的結果清理掉
    clear_folder(app.config['PROCESSED_FOLDER'])
    # 启动时异步生成题目
    threading.Thread(target=generate_questions_async, daemon=True).start()
    socketio.run(app, debug=True)
