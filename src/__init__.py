import os
import flask

from typing import Mapping

def addRoutes(app: flask.Flask | flask.Blueprint, dirname: str) -> None:
    files = [f for f in os.scandir(dirname) if f.name.endswith(".html")]

    for file in files:
        func = lambda bound=file: flask.render_template(bound.path.replace("src/templates\\", "").replace("\\", "/"))
        func.__name__ = file.name.replace(".html", "")
        app.route("/"+file.name.replace(".html", ""), methods=["GET"])(func)

def addBlueprints(app: flask.Flask | flask.Blueprint, dirname: str) -> None:
    subdirs = [f for f in os.scandir(dirname) if f.is_dir()]

    for sub in subdirs:
        bp = flask.Blueprint(sub.name, __name__, url_prefix="/"+sub.name)
        addBlueprints(bp, sub.path)
        addRoutes(bp, sub.path)

        app.register_blueprint(bp)

def create_app(testConfig: None | Mapping=None) -> flask.Flask:
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
    )

    if testConfig is None:
        app.config.from_pyfile("config.py",  silent=True)
    else:
        app.config.from_mapping(testConfig)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    addRoutes(app, "src/templates")
    addBlueprints(app, "src/templates")

    return app