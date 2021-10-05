from flask import Flask, jsonify
from jaeger_client import Config
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

import logging
import requests


def initialize_tracer():
    """
    Initializes an instance of the Jaeger tracer.
    """

    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    open_tracing_config = {"sampler": {"type": "const", "param": 1}, "logging": True}
    tracer_config = Config(open_tracing_config, service_name="trial")

    return tracer_config.initialize_tracer()


app = Flask(__name__)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
tracer = initialize_tracer()


@app.route("/")
def homepage():
    with tracer.start_span("get-python-jobs") as span:
        homepages = []
        res = requests.get("https://jobs.github.com/positions.json?description=python")
        span.set_tag("first-tag", len(res.json()))

        for result in res.json():
            try:
                homepages.append(requests.get(result["company_url"]))
            except:
                return "Unable to get site for %s" % result["company"]

    return jsonify(homepages)


if __name__ == "__main__":
    app.run(debug=True)
