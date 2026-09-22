from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "<p>Main page</p>"


@app.route("/zelda")
def zelda_quiz():
    url = "../Random Generation/index.html"
    file = open(url, "r")
    zelda_html = file.read()
    file.close()
    return zelda_html