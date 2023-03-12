"""smrti_quant_website package initializer."""
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (smrti_quant_website/config.py)
app.config.from_object('smrti_quant_website.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable INSTA485_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# for production environment:
# $ export SMRTI_SETTINGS=secret_key_config.py
# app.config.from_envvar('SMRTI_SETTINGS', silent=True)

import smrti_quant_website.views  # noqa: E402  pylint: disable=wrong-import-position
