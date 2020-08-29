from flask import Flask
from flask import request
from ebay_bs import scrape
import os
import json

k = os.environ["KEY"]

app = Flask(__name__)


@app.route("/<key>")
def parse(key):
    print("Started")
    if k == key:
        print("keys are matching")
        q_key = request.args.get("key").replace(" ", "+")
        q_page = request.args.get("page")
        results = scrape(q_key, q_page)
        if len(results) == 0:
            status_code = 404
        else:
            status_code = 200
    else:
        results = None
        status_code = 404
    return (
        json.dumps({"results": results}),
        status_code,
        {"ContentType": "application/json"},
    )
