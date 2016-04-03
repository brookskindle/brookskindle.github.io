from flask import Blueprint, current_app, render_template, redirect, url_for

from app import pages

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")
    # Rather than perform a redirect, manually call the route function. This
    # prevents the URL from being changed.
    #return page("about")
    #return redirect(url_for(".page", path="about"))

#@bp.route("/all/")
#def all():
#    """List all of our pages we've created."""
#    all_pages = list(pages)
#    return render_template("index.html", pages=all_pages)

@bp.route("/<path:path>/")
def page(path):
    """Display a markdown page

    Args:
        path: filename of page to view, without the file extension (.md)
    """
    p = pages.get_or_404(path)  # Return 404 page if page does not exist.
    return render_template("page.html", page=p)
