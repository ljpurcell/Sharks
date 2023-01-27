from flask import Flask

app = Flask(__name__)

@app.route("/<greeting>")
def hello_world(greeting):
    return f"<p>{greeting}, Lyndon!</p>"