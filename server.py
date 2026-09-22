from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main/index.html")

@app.route("/about_me")
def project_one():
    return render_template("project_one/about_me.html")

@app.route("/zelda")
def project_two():
    return render_template("project_two/zelda.html")