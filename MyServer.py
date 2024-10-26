# import Flask as flask
import flask
app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/a2sl")
def ok():
    return flask.render_template('home.html')

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)