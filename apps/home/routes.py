# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import collections
import os
from apps.config import AzureConfig
from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for, render_template
from flask_login import login_required
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
from aiohttp import ClientSession
import asyncio
import requests

from azure.storage.blob import BlobClient, ContainerClient
from apps.home import computervision

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
        return redirect(url_for('.index'))

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(url_for('.index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(os.path.join('./', filename))
        upload_blob('uploads', filename, file)
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('.index'))
    else:
        print('Allowed image types are -> png, jpg, jpeg, gif')
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(url_for('.index'))

def upload_blob(container, filename, data):
    # Create a blob client using the local file name as the name for the blob
    blob_client = AzureConfig.blob_service_client.get_blob_client(container=container, blob=filename)

    print(f'Uploading to Azure Storage as blob: {filename}')

    # Upload the created file
    blob_client.upload_blob(data)

urls = ['https://www.grandecig.com/hs-fs/hubfs/images/blog_images/2020_Blog_Images/CompareTopDietTrends.jpg?width=730&name=CompareTopDietTrends.jpg',
        'https://www.collinsdictionary.com/images/full/fruit_163436567.jpg',
        'https://www.dole.com/-/media/project/dole/produce-images/headers/dole-produce-fruit-medley.png?rev=1416123f2d094cd1b7494365948214be&hash=F89C9786C9A5F599A784D7753F82236C']

# Helper Functions

async def fetch_url(session, img_data, object):
    """Fetch the specified URL using the aiohttp session specified."""
    box = (
        object.rectangle.x, # left
        object.rectangle.y, # top
        object.rectangle.x + object.rectangle.w, # right
        object.rectangle.y + object.rectangle.h, # bottom
    )
    cropped_image = computervision.crop_image(img_data, box)
    tmpfile = f'./{hash(cropped_image.getdata())}'
    cropped_image.save(tmpfile, "JPEG")
    cropped_image = open(tmpfile, "rb")
    tag = await computervision.tag_object(AzureConfig.computervision_client, cropped_image)
    os.remove(tmpfile)
    return tag


# Routes

@blueprint.route('/async_get_urls_v2')
async def async_get_urls_v2():
    """Asynchronously retrieve the list of URLs."""
    url = urls[0]

    # 1. await Detect object from image url
    objects = await computervision.detect_objects(AzureConfig.computervision_client, url)

    # 2. crop objects
    img_data = requests.get(url).content
    async with ClientSession() as session:
        tasks = []
        for object in objects:
            if object.rectangle.w > 50 and object.rectangle.h > 50:
                task = asyncio.create_task(fetch_url(session, img_data, object))
                tasks.append(task)
        tags = await asyncio.gather(*tasks)

    object_amount = collections.Counter(tags)

    # Generate the HTML response
    response = '<h1>Food:</h1>'
    for object, amount in object_amount.items():
        response += f"<p>{object}: {amount}</p>"

    return response
