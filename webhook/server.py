import os
import sys
import logging
import docker
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


GITHUB_APIKEY = os.environ.get('GITHUB_TOKEN', None)
if GITHUB_APIKEY is None:
    sys.exit("`GITHUB_TOKEN` env var is not set")

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

logger = logging.getLogger(__name__)

client = docker.from_env()


@app.route('/', methods=['POST'])
def handle_webhook():
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == 'ping':
        logger.info('received ping')
        return dumps({'msg': 'pong'})

    logger.info("hook triggered")
    try:
        client.containers.run(
                "resume-builder:latest", auto_remove=True,
                environment={"GITHUB_TOKEN": GITHUB_APIKEY},
                detach=True,
                volumes={'/volume1/web/': {'bind': '/out', 'mode': 'rw'}})
    except Exception as e:
        print("Error:", e)
        return str(e), 500
    return '', 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
