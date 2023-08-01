let chatSocket

    function submitRoom(){
        let roomName = document.getElementById('roomName').value
        let url = `ws://${window.location.host}/ws/chat/${roomName}`
        chatSocket = new WebSocket(url)
        console.log(url)
        chatSocket.onmessage = function (e) {
            let data = JSON.parse(e.data)
            console.log('Data:', data)

            if (data.type === 'chat') {
                let messages = document.getElementById('messages')
                messages.insertAdjacentHTML('beforeend', '<div><p>' + data.message + '</p></div>')
            }
        }

    }

    function submitMessage(){
        let message = document.getElementById('message').value
        chatSocket.send(JSON.stringify({
            'message': message
        }))
        document.getElementById('message').value = ""
    }
