from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query = request.form['query']
    response = requests.get('https://46c1-103-21-79-9.ap.ngrok.io/ask_bot', params={'query': query})
    response_data = response.json()

    return render_template('response.html', response=response_data['response'])

if __name__ == '__main__':
    app.run(debug=True)
