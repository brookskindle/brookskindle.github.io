from flask import Flask
from flask_flatpages import FlatPages
from flask_bootstrap import Bootstrap

pages = FlatPages()
bootstrap = Bootstrap()

def create_app(config_file):
    """Create a flask application from a configuration file.

    Args:
        config_file: Filename of a config file to load app config values from.
                     Must be relative to this directory.

    Returns:
        An initialized flask application
    """
    # App initialization
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # Other initialization
    pages.init_app(app)
    bootstrap.init_app(app)

    # Route registration
    from app.main.views import bp as main_bp
    app.register_blueprint(main_bp)
    from app.blog.views import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix="/blog")

    return app
