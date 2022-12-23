import json
from flask import Flask, request, jsonify
from vehicle_command_controller import VehicleCommandController
from vehicle_command_controller import ControllerException
from vehicle_command_controller import BadMethodException
import threading
import os

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return "hello world"


@app.route('/vehicle-command', methods=['POST'])
def vehicle_command():
    request_body_json = request.get_json()
    method = request.method
    path = request.path
    query_params = request.args

    [status_code, response_body] = dispatch_method(
        method, path,
        request_body_json,
        query_params
    )

    return jsonify(response_body), status_code


def dispatch_method(method, path, params, query_params):
    try:
        if not method == 'POST':
            raise BadMethodException(f'HTTP {method} not supported')
        ctrl = VehicleCommandController()
        ctrl.post_command(params)
        ctrl.execute_command()
        return ctrl.response
    except ControllerException as ex:
        return (ex.status_code, {"error": str(ex)})


if __name__ == '__main__':
    app.run(port=9000)
