from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/metrics")
def metrics():
    return render_template("metrics.html")

if __name__ == "__main__":
    app.run(debug=True)
