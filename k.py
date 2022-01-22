import threading

import flask

app = flask.Flask("a")


@app.route("/")
def a():
    return "a"


def r():
    app.run("0.0.0.0", 80)


def k():
    threading.Thread(target=r).start()
