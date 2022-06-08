import os
import yaml
import logging

from worker.services.auth import fetch_backend_url_firestore


usingProjectId = os.getenv('project_id', 'local')


def get_logging_level():
    return os.getenv("LOGGING_LEVEL", "INFO")


def configure_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(module)s]: #%(funcName)s @%(lineno)d: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": get_logging_level(), "handlers": ["wsgi"]},
        }
    )


def read_config():
    if usingProjectId == "local":
        yaml_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(yaml_file_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    else:
        return {
            'backend_endpoint': [
              f"{fetch_backend_url_firestore()}/api/v1/execute_bot_signal",
            ]
        }
    

config = read_config()
