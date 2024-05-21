let recordButton = document.getElementById('recordButton');
let stopButton = document.getElementById('stopButton');

let mediaRecorder;
let audioChunks = [];
let audioStream;

recordButton.addEventListener('click', async () => {
    // 获取音频流
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(audioStream);
    
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
        let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        audioChunks = []; // 清空音频数据

        let formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');
        
        // 将音频文件发送到后端
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
    
    mediaRecorder.start();
    recordButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    // 停止音频流
    audioStream.getTracks().forEach(track => track.stop());
    recordButton.disabled = false;
    stopButton.disabled = true;
});
