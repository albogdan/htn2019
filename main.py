import os
import json

"""This is the routing file - all pages of website will be directed from here"""
from application import create_app, cli

# Create the flask application
flask_app = create_app()

# Register custom CLI commands
cli.register(flask_app)

# if __name__ == "__main__":
#     flask_app.run(host='192.168.1.214', port=8081)

if __name__ == "__main__":
    flask_app.run(host='127.0.0.1', port=8080)
