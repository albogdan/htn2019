#from application import flask_app

import click
import os


"""
Encapsulate the commands in a function to be able to register it with the application
and pass different parameters if the need arises
"""
def register(flask_app):
    @flask_app.cli.group()
    def seed():
        """Seeding commands for database tables for frosh groups, etc"""
        pass

    @seed.command()
    def a():
        print("a")