import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import uuid
import whisper
import glob
from chatGPT import getGptResponse
from soVITS_api import getVitsResponse

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/recordings/'
app.config['PROCESSED_FOLDER'] = 'static/output/'
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

last_output_filename = None

def speach_to_text(filepath):
    model = whisper.load_model("medium")
    audio = whisper.pad_or_trim(whisper.load_audio(filepath))
    result = whisper.transcribe(model, audio, language='zh')
    return result['text']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global last_output_filename
    
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
        user_input_text = speach_to_text(filepath = recording_file_path)
        print(user_input_text)

        # 取得 gpt 回應 (return 純文字)
        assistant_response = getGptResponse(user_input_text)
        print(assistant_response)

        # 文字轉語音處理 (return BytesIO物件)
        output_bytesIO = getVitsResponse(assistant_response)

        # 使用唯一文件名(避免瀏覽器快取一直讀到同一個檔案)
        unique = str(uuid.uuid4())
        output_filename = 'output_' + unique + '.wav'
        output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        with open(output_filepath, "wb") as f:
            f.write(output_bytesIO.read())

        # 删除上次處理的文件
        if last_output_filename:
            last_output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], last_output_filename)
            if os.path.exists(last_output_filepath):
                os.remove(last_output_filepath)
        
        # 更新上次處理的文件名
        last_output_filename = output_filename
        
        # 通知前端
        socketio.emit('processing_done', {'filename': output_filename})
        return 'File successfully uploaded', 200

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# 將指定路徑下的檔案刪除
def clear_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    # 執行程式前先將之前的結果清理掉
    clear_folder('static/output/')
    socketio.run(app, debug=True)
