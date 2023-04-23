from flask import Blueprint

query = Blueprint("query", __name__)

import osrs.routes.queries
