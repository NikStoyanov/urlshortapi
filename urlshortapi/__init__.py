from flask import Flask
app = Flask(__name__)

import urlshortapi.api  # noqa: F401
