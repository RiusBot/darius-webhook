import logging
from flask import request, jsonify
from functools import wraps


def validate_empty_fields(fields, json_payload, errors):
    for field in fields:
        if json_payload.get(field) is None:
            errors.append(f"'{field}' should not be empty")


def validate_string_fields(fields, json_payload, errors):
    for field in fields:
        if field not in json_payload.keys():
            continue
        if not isinstance(json_payload.get(field), str):
            errors.append(f"'{field}' must be a string")


def validate_numeric_fields(fields, json_payload, errors):
    for field in fields:
        if field not in json_payload.keys():
            continue
        if not isinstance(json_payload.get(field), (float, int)):
            errors.append(f"'{field}' must be a number")


def validate_dict_fields(fields, json_payload, errors):
    for field in fields:
        if field not in json_payload.keys():
            continue
        if not isinstance(json_payload.get(field), dict):
            errors.append(f"'{field}' must be a number")


def apply_fields_validators(data, mandatory_fields, string_fields, numeric_fields, dict_fields):
    errors = list()
    validate_length_fields(mandatory_fields, data, errors)
    if not errors:
        validate_empty_fields(mandatory_fields, data, errors)
        validate_string_fields(string_fields, data, errors)
        validate_numeric_fields(numeric_fields, data, errors)
        validate_dict_fields(dict_fields, data, errors)
    return errors


def validate_length_fields(fields, json_payload, errors):
    for field in fields:
        if field not in json_payload.keys():
            continue
        if len(json_payload.get(field)) > 36:
            errors.append(f"'{field}' length exceeded")


def main_validator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        mandatory_fields = ["current_price", "sentiment_stats", "sentiment_status", "rolling_apy", "action"]
        string_fields = ["current_price", "sentiment_stats", "sentiment_status", "rolling_apy", "action"]
        numeric_fields = []
        dict_fields = []
        data = request.get_json()
        if data is None:
            error_message = "empty request body"
            logging.error(error_message)
            return jsonify({"error_messages": error_message}), 400

        errors = apply_fields_validators(data, mandatory_fields, string_fields, numeric_fields, dict_fields)

        if errors:
            logging.error(str(errors))
            return jsonify({"error_messages": errors}), 400
        return f(*args, **kwargs)

    return wrapper


def acdc_validator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        mandatory_fields = ["instId", "access_token", "strategy", 'side', 'ordType', 'slTriggerPx', 'tpTriggerPx']
        string_fields = ["instId", "access_token", "strategy", 'side', 'ordType', 'slTriggerPx', 'tpTriggerPx', 'sz']
        numeric_fields = []
        dict_fields = []
        data = request.get_json()
        if data is None:
            error_message = "empty request body"
            logging.error(error_message)
            return jsonify({"error_messages": error_message}), 400

        errors = apply_fields_validators(data, mandatory_fields, string_fields, numeric_fields, dict_fields)

        if errors:
            logging.error(str(errors))
            return jsonify({"error_messages": errors}), 400
        return f(*args, **kwargs)

    return wrapper


def webhook_validator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        mandatory_fields = ["symbol", "action"]
        string_fields = ["symbol", "action"]
        numeric_fields = []
        dict_fields = []
        data = request.get_json()
        if data is None:
            error_message = "empty request body"
            logging.error(error_message)
            return jsonify({"error_messages": error_message}), 400

        errors = apply_fields_validators(data, mandatory_fields, string_fields, numeric_fields, dict_fields)

        if errors:
            logging.error(str(errors))
            return jsonify({"error_messages": errors}), 400
        return f(*args, **kwargs)

    return wrapper
