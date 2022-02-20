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

# Food Routes

@blueprint.route('/food_create', methods=['POST'])
@login_required
def food_post():
    name = request.form.get('food')
    expiration = request.form.get('expiration_date')
    quantity = request.form.get('quantity')

    # create a new food item
    new_food = Foods(
        name=name, 
        quantity=quantity,
        expiration_date=expiration,
        id_user=current_user.id)

    # add the new user to the database
    db.session.add(new_food)
    db.session.commit()

    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/food_update/<int:id>', methods=['POST'])
@login_required
def food_update(id):
    food = Foods.query.filter_by(id=id).first()
    food.name = request.form.get('food')
    food.expiration_date = request.form.get('expiration_date')
    food.quantity = request.form.get('quantity')

    db.session.commit()

    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/food_delete/<int:id>', methods=['POST'])
@login_required
def food_delete(id):
    my_data = Foods.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Item deleted successfully.")

    return redirect(url_for("home_blueprint.index"))


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
