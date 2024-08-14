from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

broadcaster: WebSocket = None  # Store the broadcaster connection
viewers: List[WebSocket] = []  # Store viewer connections


@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Video Stream</title>
        </head>
        <body>
            <h1>WebSocket Video Stream</h1>
            <p>Select role: 
               <a href="/broadcast">Broadcast</a> | 
               <a href="/view">View</a>
            </p>
        </body>
    </html>
    """)

@app.get("/broadcast")
async def broadcast():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Broadcast Video Stream</title>
        </head>
        <body>
            <h1>Broadcast Video Stream</h1>
            <video id="video" width="640" height="480" autoplay></video>
            <script>
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function(stream) {
                        let video = document.getElementById('video');
                        video.srcObject = stream;

                        let websocket = new WebSocket('ws://127.0.0.1:8000/ws/broadcast');
                        websocket.onopen = function() {
                            let mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
                            mediaRecorder.ondataavailable = function(event) {
                                if (event.data.size > 0) {
                                    websocket.send(event.data);
                                }
                            };
                            mediaRecorder.start(100); // Send data every 100ms
                        };
                    })
                    .catch(function(error) {
                        console.error("Error accessing media devices.", error);
                    });
            </script>
        </body>
    </html>
    """)

@app.get("/view")
async def view():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>View Video Stream</title>
        </head>
        <body>
            <h1>View Video Stream</h1>
            <video id="video" width="640" height="480" autoplay></video>
            <script>
                let video = document.getElementById('video');
                let websocket = new WebSocket('ws://127.0.0.1:8000/ws/view');

                websocket.binaryType = 'blob';

                websocket.onmessage = function(event) {
                    if (event.data instanceof Blob) {
                        let url = URL.createObjectURL(event.data);
                        video.src = url;
                    } else {
                        console.error('Received non-blob data.');
                    }
                };

                websocket.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws/broadcast")
async def broadcast_stream(websocket: WebSocket):
    global broadcaster
    if broadcaster is not None:
        await websocket.close()
        return
    
    broadcaster = websocket
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_bytes()
            # Broadcast to all viewers
            for viewer in viewers:
                await viewer.send_bytes(data)
    except WebSocketDisconnect:
        broadcaster = None
        print("Broadcaster disconnected")

@app.websocket("/ws/view")
async def view_stream(websocket: WebSocket):
    await websocket.accept()
    viewers.append(websocket)
    
    try:
        while True:
            await websocket.receive_text()  # Keep the connection open
    except WebSocketDisconnect:
        viewers.remove(websocket)
        print("Viewer disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
