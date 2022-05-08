function task_status(task_type) {
    var socket = new WebSocket("ws://127.0.0.1:8000/ws/collect/");

    socket.onmessage = function(event) {
        var collect = event.data;
        document.querySelector("#response_output").innerText = collect;
    }
}

task_status()
