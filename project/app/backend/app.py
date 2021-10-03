import logging
from jaeger_client import Config
from opentracing.ext import tags
from opentracing.propagation import Format

from flask import Flask, render_template, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

import pymongo
from flask_pymongo import PyMongo


def init_tracer(service):
    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    config = Config(
        config={
            "sampler": {
                "type": "const",
                "param": 1,
            },
            "logging": True,
        },
        service_name=service,
    )
    # this call also sets opentracing.tracer
    return config.initialize_tracer()


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

metrics = PrometheusMetrics(app)
tracer = init_tracer("backend")


@app.route("/")
def homepage():
    with tracer.start_span("home-span") as span:
        span.set_tag("http.method", request)
        return "Hello World"


@app.route("/api")
def my_api():
    with tracer.start_span("api-span") as span:
        answer = "something"
        span.set_tag("http.method", request)
        return jsonify(response=answer)


@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span("star-span") as span:
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        star_id = star.insert({"name": name, "distance": distance})
        new_star = star.find_one({"_id": star_id})
        output = {"name": new_star["name"], "distance": new_star["distance"]}

        span.set_tag("http.method", request)
        return jsonify({"result": output})


if __name__ == "__main__":
    app.run()
