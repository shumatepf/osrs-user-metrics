from flask import Blueprint

query = Blueprint("query", __name__)
index = Blueprint("index", __name__)

import osrs.routes.queries
import osrs.routes.indices
