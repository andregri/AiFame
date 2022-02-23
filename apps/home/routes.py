# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

from apps.food_inventory.models import Foods
from apps.food_inventory.forms import FoodForm

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index') 

@blueprint.route('/<template>')
@login_required
def route_template(template):
    table = Foods.query.all()
    form = FoodForm(request.form)

    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, table=table, form=form)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home_blueprint.index'))
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(url_for('home_blueprint.index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('./', filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template(url_for('home_blueprint.index'), filename=filename)
    else:
        print('Allowed image types are -> png, jpg, jpeg, gif')
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(url_for('home_blueprint.index'))