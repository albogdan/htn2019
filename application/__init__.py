import os

# Import flask and template operators
from flask import Flask, render_template

# Import dash and dependencies
import dash
from flask.helpers import get_root_path

# Import SQLAlchemy and Migrate
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from config import ProductionConfig, DevelopmentConfig

# Import the flask-login authentication module
#from flask_login import LoginManager, login_required

from flask_materialize import Material

# Initialize the database instance for storing all the information
#db = SQLAlchemy()

# Initialize the database migrate instance
#migrate = Migrate()

# Initialize the login instance
#login_manager = LoginManager()
"""
 Encapsulate the app in a function in order to be able to initialize it with
 various environment variables for  testing as well as versatility
"""
# DASH SETUP : https://github.com/okomarov/dash_on_flask/tree/feature/multiple_dash_apps
def create_app():
    
    flask_app = Flask(__name__)
    # Change to production configuration if in production
    if(os.environ['ENVIRONMENT'] == 'PRODUCTION'):
        config_class=ProductionConfig()
    else:
        config_class=DevelopmentConfig()


    # Define the application object
    flask_app = Flask(__name__)

    # Configurations taken from function argument
    flask_app.config.from_object(config_class)

    # Initialize the various models with the flask_app
    #db.init_app(flask_app)
    #migrate.init_app(flask_app, db)

    # Create a LoginManager instance
    #login_manager.init_app(flask_app)
    #login_manager.login_view = 'auth.login'
    #login_manager.login_message= ''

    # Sample HTTP error handling
    @flask_app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404


    # Setup the DASH apps
    from application.visualizer.layout import layout as layout
    from application.visualizer.callbacks import register_callbacks as register_callbacks
    register_dashapp(flask_app, 'Visualizer 1', 'visualizer', layout, register_callbacks)


    # Import a module / component using its blueprint handler variable (mod_auth)
    #from application.mod_auth.controllers import mod_auth as auth_module
    from application.home import home as home_module
    #from application.visualizer import dash as dash_visualizer

    # Register blueprint(s) - connects each module to the main flask application
    # app.register_blueprint(xyz_module)

    flask_app.register_blueprint(home_module)
    #flask_app.register_blueprint(auth_module)
    #flask_app.register_blueprint(dash_module)

    return flask_app

def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    my_dashapp = dash.Dash(__name__, server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           external_stylesheets=external_stylesheets)

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    #_protect_dashviews(my_dashapp)

# def _protect_dashviews(dashapp):
#    for view_func in dashapp.server.view_functions:
#         if view_func.startswith(dashapp.config.url_base_pathname):
#             dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])
    # for view_func in dashapp.server.view_functions:
    #     print(view_func)
    #     if view_func.startswith(dashapp.url_base_pathname):
    #         dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


#from application import db_models

# Import the custom Command Line Interface file for custom flask commands
from application import cli
