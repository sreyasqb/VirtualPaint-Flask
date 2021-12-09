from flask import Flask,render_template,url_for,Response
app= Flask(__name__)

@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/vpaint")
def index():
    import virtualPaint
    return render_template("index.html")


if __name__== '__main__':
    app.run(debug=True)