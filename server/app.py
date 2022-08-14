from flask import Flask, request, jsonify
from flask_cors import CORS
from crypto_bot import start_bot, stop_bot
from commands import *
import sys

app = Flask(__name__)

# Set up Flask to bypass CORS at the front end
cors = CORS(app)


@app.route("/receiver", methods=["POST"])
def postME():
    data = request.get_json()
    data = jsonify(data)
    return data


@app.route("/start", methods=["POST"])
def run_bot():
    start_bot()
    opened = jsonify("OK")
    return opened


@app.route("/end", methods=["POST"])
def end_bot():
    stop_bot()
    # closed = jsonify({"response": "Stopped Trading Bot"})
    closed = jsonify("Stopped Trading Bot")
    return closed


@app.route("/account", methods=["POST"])
def account_info():
    result = get_account_info()
    return result


# Run the app:
if __name__ == "__main__":
    app.run(debug=True)
