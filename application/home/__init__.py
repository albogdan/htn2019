from flask import Blueprint

# Create the home Blueprint
home = Blueprint('home', __name__, url_prefix='/')

from application.home import controllers
