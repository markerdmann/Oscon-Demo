from flask import Flask, request, render_template
from redis import Redis
import cjson

app = Flask(__name__)

if __name__ == '__main__':
    redis = Redis()
    app.debug = True
else:
    with open('/home/dotcloud/environment.json') as f:
        config = cjson.decode(f.read())
    redis = Redis(host=config['DOTCLOUD_REDIS_REDIS_HOST'],
                  port=int(config['DOTCLOUD_REDIS_REDIS_PORT']),
                  password=config['DOTCLOUD_REDIS_REDIS_PASSWORD'])

@app.route('/new_message', methods=['POST'])
def new_message():
    body = request.form['Body']
    redis.set('latest_message', body)
    return 'Success!'

@app.route('/latest_message')
def latest_message():
    msg = redis.get('latest_message') or 'No message yet!'
    return msg

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(port=3001)
else:
    application = app.wsgi_app

