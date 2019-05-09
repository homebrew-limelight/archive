from flask import Flask, render_template, url_for, send_from_directory, request

app = Flask(__name__)


@app.route('/')
def test():
    return send_from_directory("static","test.html")

@app.route('/',methods=['POST'])
def test_post():
    print(request.form['value'])
    return 'yeet'


if __name__ == '__main__':
    app.run()
