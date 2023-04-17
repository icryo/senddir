from flask import Flask, request
import base64
import time
from threading import Thread

app = Flask(__name__)

def mark_expired(content):
    time.sleep(600)
    print('Item expired:', content)

@app.route('/', methods=['GET'])
def process():
    content_encoded = request.args.get('content')
    if content_encoded:
        content_decoded = base64.b64decode(content_encoded).decode('utf-8')
        print(f"\033[32m{content_decoded}\033[0m")  # print in green
        t = Thread(target=mark_expired, args=(content_decoded,))
        t.start()
        return f"Processed content: <span style='color: green'>{content_decoded}</span>"
    else:
        return 'Please provide content parameter'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
