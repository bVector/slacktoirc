from flask import Flask, request
import redis

from keys import token

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    r = redis.Redis()
    if request.form['user_name'] == 'slackbot': return ''
    if request.form['token'] == token:
        print 'valid request'
        name = str(request.form['user_name'])
        text = str(request.form['text'])
        line = name + ': ' + text
        r.lpush('slacktoirc', line)
        print name, text
    else:
        print 'invalid', str(request.form)
    return '' 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
