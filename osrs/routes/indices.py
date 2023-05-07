from flask import render_template, send_from_directory
from osrs.routes import index

from osrs import settings

@index.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@index.route('/assets/<path:path>')
def static_stuff(path):
    return send_from_directory('assets/', path)