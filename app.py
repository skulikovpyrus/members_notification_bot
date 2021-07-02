from flask import Flask
from flask import request, Response
from bot import NotificationBot
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.data:
        data = json.loads(request.data.decode("utf-8"))

        task = data["task"]
        token = data["access_token"]
        settings = json.loads(data["bot_settings"])

        bot = NotificationBot(task, token, settings)
        bot.main()

    return Response(status=200)


if __name__ == "__main__":
    app.run()
