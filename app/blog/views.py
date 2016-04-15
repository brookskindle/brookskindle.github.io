from flask import Blueprint, render_template, current_app

from app import pages

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    return render_template("blog.html")

@bp.route("/<path:path>/")
def post(path):
    """Show a specific blog post

    Args:
        path: name of the blog post to view, without a file extention.
    """
    page = pages.get_or_404(path)
    return render_template("post.html", post=page)
