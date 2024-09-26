// DOM elements
const characterResponses = document.getElementById('character-responses');
const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const startVoiceBtn = document.getElementById('start-voice-btn');
const stopVoiceBtn = document.getElementById('stop-voice-btn');
const audioPlayer = document.getElementById('audioPlayer');
const feedbackMessage = document.getElementById('feedbackMessage');

// Voice recording variables
let mediaRecorder;
let audioChunks = [];
const socket = io();
let audioQueue = [];
let textQueue = [];
let userQueue = [];
let isPlaying = false;
let sid = null;

// Function to send user message (both text and transcribed voice input)
function sendMessage(message, isVoiceInput = false) {
    if (message.trim()) {
        // Display user message in chatroom
        appendMessage(message, 'user-message');
    }
}

// Append message to the chat window
function appendMessage(content, messageType) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', messageType);
    messageElement.innerText = content;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Start voice recording
startVoiceBtn.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        const filename = 'recording.wav'; // Fixed filename for simplicity
        formData.append('file', audioBlob, filename);

        // Send recorded audio to backend
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            if (result.status === 'upload_success' && sid) {
                await fetch('/start_tts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ sid })
                });
            }
        } else {
            console.error('Error uploading file');
        }
    };

    mediaRecorder.start();
    startVoiceBtn.disabled = true;
    stopVoiceBtn.disabled = false;
});

// Stop voice recording
stopVoiceBtn.addEventListener('click', () => {
    mediaRecorder.stop();
    startVoiceBtn.disabled = false;
    stopVoiceBtn.disabled = true;
    audioChunks = [];
    // 視覺回饋：顯示提示訊息
    feedbackMessage.textContent = "錄音已停止";
});

// Socket events handling
socket.on('user_input', data => {
    const transcribedText = data.text;

    // Add the transcribed voice input as a user message in the chatroom
    sendMessage(transcribedText, true);
});

socket.on('tts_done', data => {
    const ttsAudio = data.file;
    const ttsText = data.text;

    // Append the TTS text response as a character's message in the chatroom
    appendMessage(ttsText, 'character-message');

    // Play the audio file
    audioQueue.push(ttsAudio);
    playNext();
});

socket.on('sid', data => {
    sid = data.sid;
});

let selectedModel = null
// Play the TTS audio sequentially
function playNext() {
    if (!isPlaying && audioQueue.length > 0) {
        feedbackMessage.textContent = "";
        // 在首次播放時隨機選擇 modelPaths[6] 或 modelPaths[7]
        if (selectedModel === null) {
            console.log('changemodel')
            const randomNum = Math.random(); // 生成 0 到 1 之間的隨機數
            if (randomNum < 0.5) {
                selectedModel = modelPaths[7];
                console.log(randomNum)
            } else {
                selectedModel = modelPaths[6];
            }
            loadModel(selectedModel); // 加載隨機選擇的模型
        }
        isPlaying = true;
        const audioSrc = audioQueue.shift();
        const audio = new Audio(audioSrc);
        audio.play();

        audio.onended = () => {
            isPlaying = false;
            // 當 audioQueue 清空，表示這次對話已結束
            if (audioQueue.length === 0) {
                // 切換回 modelPaths[0]
                loadModel(modelPaths[0]);
                selectedModel = null; // 重置模型選擇，以便下次對話重新選擇
            } else {
                // 繼續播放下一段對話
                playNext();
            }
        };
    }
}

// Event listeners for text input and sending
sendBtn.addEventListener('click', () => sendMessage(userInput.value));
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage(userInput.value);
        text_backend(userInput.value);
        userInput.value = '';
    }
});

function text_backend(message) {
    fetch('/text_backend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

