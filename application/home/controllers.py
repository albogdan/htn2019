from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from datetime import datetime

# Import files for logging in


# Import the homepage Blueprint from home/__init__.py
from application.home import home


@home.route('/')
@home.route('/index')
def index():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d, %B, %Y at %X")
    content = "Hello, the time is " + formatted_now
    return render_template('home/index.html', key=formatted_now)

    
@home.route('/visualize')
def visualizer():
    return redirect('visualizer')

@home.route('/survey')
def survey():
    return redirect('survey')