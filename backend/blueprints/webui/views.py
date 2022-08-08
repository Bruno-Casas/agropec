from flask import render_template

def index():
    partiu = 'Bora codar!!!'
    return render_template('index.html', partiu = partiu)