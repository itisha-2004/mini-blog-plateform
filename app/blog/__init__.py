from flask import Blueprint

# Define blueprint here
blog_bp = Blueprint('blog', __name__)

# Import routes to register them with the blueprint
from . import routes  # keep this last
