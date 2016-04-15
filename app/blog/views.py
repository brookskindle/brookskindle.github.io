from flask import Blueprint, render_template, current_app

from app import pages

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    posts = [p for p in pages if p.meta.get("date")]
    sorted_posts = sorted(  # Sort posts by most recent first
        posts,
        key=lambda post: post.meta["date"],
        reverse=True
    )
    return render_template("blog.html", posts=sorted_posts)

@bp.route("/<path:path>/")
def post(path):
    """Show a specific blog post

    Args:
        path: name of the blog post to view, without a file extention.
    """
    page = pages.get_or_404(path)
    return render_template("post.html", post=page)
