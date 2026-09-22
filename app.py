from flask import Flask, render_template, redirect
from minecraft_manager import start_server, stop_server, processes

app = Flask(__name__)


@app.route("/")
def index():
    running = "survival" in processes

    return render_template(
        "index.html",
        running=running
    )


@app.post("/server/start")
def start():
    start_server()
    return redirect("/")


@app.post("/server/stop")
def stop():
    stop_server()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
