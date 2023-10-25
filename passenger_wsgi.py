from app import socketio, MyApp

if __name__ == "__main__":
        socketio.run(MyApp, debug=True)