document.addEventListener('DOMContentLoaded', function() {
    var messageTimeout = document.getElementById('message-timeout');
    if (messageTimeout) {
        setTimeout(function(){
            messageTimeout.style.display = 'none';
        }, 3000);
    }
});