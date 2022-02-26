# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required
)

from apps import db, login_manager
from apps.food_inventory import blueprint
from apps.food_inventory.models import Foods
from apps.food_inventory.forms import FoodForm

# Food Routes
    
@blueprint.route('/food_create', methods=['POST'])
@login_required
def food_post():
    form = FoodForm(request.form)

    if not form.validate_on_submit():
        flash("Invalid data")
        return redirect(url_for('home_blueprint.route_template', template='tables'))

    name = form.food_name.data
    expiration = form.expiration_date.data
    quantity = form.quantity.data

    # create a new food item
    new_food = Foods(
        name=name, 
        quantity=quantity,
        expiration_date=expiration,
        id_user=current_user.id
    )

    # add the new user to the database
    db.session.add(new_food)
    db.session.commit()

    return redirect(url_for('home_blueprint.route_template', template='tables'))

@blueprint.route('/food_update/<int:id>', methods=['POST'])
@login_required
def food_update(id):
    food = Foods.query.filter_by(id=id).first()

    form = FoodForm(request.form)

    if not form.validate_on_submit():
        flash("Invalid data")
        return redirect(url_for('home_blueprint.route_template', template='tables'))

    food.name = form.food_name.data
    food.expiration = form.expiration_date.data
    food.quantity = form.quantity.data

    db.session.commit()

    return redirect(url_for('home_blueprint.route_template', template='tables'))

@blueprint.route('/food_delete/<int:id>', methods=['POST'])
@login_required
def food_delete(id):
    my_data = Foods.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Item deleted successfully.")

    return redirect(url_for('home_blueprint.route_template', template='tables'))

@blueprint.route('/add_foods_from_image', methods=['POST'])
@login_required
def add_food_from_image():
    foods = request.json
    for food in foods:
        row = Foods.query.filter_by(name=food['name']).first()
        if row:
            # If exists, update
            row.name = food['name']
            row.quantity = food['quantity']
            row.expiration_date = food['expiration_date']
        else:
            # if not exists, create
            new_food = Foods(
                name=food['name'], 
                quantity=food['quantity'],
                expiration_date=food['expiration_date'],
                id_user=current_user.id
            )
            db.session.add(new_food)
        
        db.session.commit()
    
    return redirect(url_for('home_blueprint.route_template', template='tables'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500 
