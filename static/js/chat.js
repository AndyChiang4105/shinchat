document.addEventListener('DOMContentLoaded', function() {
    var messages = [
        { text: "12345。", side: "left" },
        { text: "12345。", side: "right" }
    ];
    
    var chatContent = document.getElementById('chat-content');
    
    function addMessage(message, side) {
        var messageDiv = document.createElement('div');
        messageDiv.className = side === 'right' ? 'message-right' : 'message-left';
        chatContent.appendChild(messageDiv);

        let i = 0;
        function typeMessage() {
            if (i < message.length) {
                messageDiv.textContent += message.charAt(i);
                i++;
                setTimeout(typeMessage, 100); // 每個字母間的延遲時間，可以根據需要調整
            }
        }
        typeMessage();
    }
    
    function displayMessages(index) {
        if (index < messages.length) {
            var message = messages[index];
            addMessage(message.text, message.side);
            setTimeout(function() {
                displayMessages(index + 1);
            }, message.text.length * 100 + 500); // 根據訊息長度設置延遲時間
        }
    }

    displayMessages(0);
});
