from flask import Flask, jsonify, request
from flask_opentracing import FlaskTracer
from flask_pymongo import PyMongo
from jaeger_client import Config
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

import json
import logging
import opentracing


def initialize_tracer():
    """
    Initializes an instance of the Jaeger tracer.
    """

    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    open_tracing_config = {"sampler": {"type": "const", "param": 1}, "logging": True}
    tracer_config = Config(open_tracing_config, service_name="backend")

    return tracer_config.initialize_tracer()


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"
mongo = PyMongo(app)

flask_tracer = FlaskTracer(initialize_tracer, True, app)
flask_tracer_span = flask_tracer.get_span()

metrics = GunicornInternalPrometheusMetrics(app)


@app.route("/")
def homepage():
    with opentracing.tracer.start_span(
        "home-endpoint", child_of=flask_tracer_span
    ) as span:
        response = {"message": "Home endpoint"}
        span.set_tag("message", response)

        return jsonify(response)


@app.route("/api")
def my_api():
    with opentracing.tracer.start_span(
        "api-endpoint", child_of=flask_tracer_span
    ) as span:
        response = {"message": "API endpoint"}
        span.set_tag("message", response)

        return jsonify(response)


@app.route("/star", methods=["POST"])
def add_star():
    with opentracing.tracer.start_span(
        "star-endpoint", child_of=flask_tracer_span
    ) as span:
        try:
            star = mongo.db.stars
            name = request.json["name"]
            distance = request.json["distance"]
            star_id = star.insert({"name": name, "distance": distance})
            new_star = star.find_one({"_id": star_id})
            output = {"name": new_star["name"], "distance": new_star["distance"]}

            response = jsonify({"result": output})
            span.set_tag("message", json.dumps(response))

            return response
        except:
            span.set_tag("response", "Can't retrieve output from database")


if __name__ == "__main__":
    app.run()
