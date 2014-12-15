#! /usr/bin/env python
from flask import Flask, request
import redis
from dogapi.stats import DogStatsApi

from keys import token, dogkey

app = Flask(__name__)
dog = DogStatsApi()
dog.start(api_key=dogkey)
dog.increment('slacktoirc.start', tags=['flask', 'slack', 'webhook'])

@app.route('/', methods=['POST'])
def hello_world():
    
    r = redis.Redis()
    if request.form['user_name'] == 'slackbot': 
        dog.increment('slacktoirc.ignored')
        return ''
    if request.form['token'] == token:
        dog.increment('slacktoirc.valid')
        print 'valid request'
        name = str(request.form['user_name'])
        text = str(request.form['text'])
        line = name + ': ' + text
        r.lpush('slacktoirc', line)
        dog.increment('slacktoirc.name.%s'%(name))
        print name, text
    else:
        print 'invalid', str(request.form)
        dog.increment('slacktoirc.invalid')
    return '' 

if __name__ == '__main__':

#    app.debug = True
    app.run(host='0.0.0.0', port=8989)
