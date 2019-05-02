from flask import Flask, render_template, url_for, send_from_directory, request
import socket

app = Flask(__name__)

host = '127.0.0.1'
port = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
conn, addr = s.accept()

@app.route('/')
def test():
    return send_from_directory("static","test.html")

@app.route('/',methods=['POST'])
def send_data():
    data = request.form['value']
    data_enc = data.encode('utf-8')
    conn.send(data_enc)
    return data

if __name__ == '__main__':
    app.run()
