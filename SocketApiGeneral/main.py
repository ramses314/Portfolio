import socketio
from fastapi import FastAPI

from src.routes.ws_no_prefix import sio


app = FastAPI()
sio_asgi_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)
app.add_route("/socket.io/", route=sio_asgi_app, methods=["GET", "POST"])
app.add_websocket_route("/socket.io/", sio_asgi_app)


@app.get("/hello")
async def root():
    await sio.emit("response", "hello everyone")
    return {"message": "hello"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
