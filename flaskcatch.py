from flask import Flask, request
import base64
import time
from threading import Thread
import re

app = Flask(__name__)

def mark_expired(content, expiry_time=600):
    time.sleep(expiry_time)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - Item expired: {content} \U0001F635")

    

@app.route('/', methods=['GET'])
def process():
    content_encoded = request.args.get('content')
    if content_encoded:
        content_decoded = base64.b64decode(content_encoded).decode('utf-8')
        if re.search(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])', content_decoded) or re.search(r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])', content_decoded):
            print(f"\U0001F511 \033[95m  AWS key  \U0001F511 \n{content_decoded}\033[0m")  # print in hot pink with label
            color_style = "color: hotpink"
            print ('')
        else:
            print(f"\033[32m{content_decoded}\033[0m")  # print in green
            color_style = "color: green"
        t = Thread(target=mark_expired, args=(content_decoded,))
        t.start()
        return f"Processed content: <span style='{color_style}'>{content_decoded}</span>"
    else:
        return 'Please provide content parameter'
print ('\U0001F603')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 
