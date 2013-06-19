# -*- coding: utf-8 -*-
"""
    about
    ~~~~~~

    「關於我」的部份

"""


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

about = Blueprint('about', __name__)


@about.route('/me')
def me():
    try:
        return render_template('about/me.html')
    except TemplateNotFound:
        abort(404)

@about.route('/site')
def site():
	return render_template('about/site.html')