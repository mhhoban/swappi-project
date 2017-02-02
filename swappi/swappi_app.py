from flask import Flask


app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def helloWorld():
    return "Shalom, World!"

if __name__ == '__main__':

    app.debug = True
    app.run(host='localhost', port=8080)