from flask import Flask
from flask import request, Response
import json
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.data:
        data = json.loads(request.data.decode("utf-8"))

        task = data["task"]
        token = data["access_token"]

    return Response(status=200)


if __name__ == "__main__":
    app.run()
