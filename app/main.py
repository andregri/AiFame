from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Food

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    table = Food.query.all()
    return render_template('profile.html', name=current_user.name, table=table)

@main.route('/profile', methods=['POST'])
@login_required
def food_post():
    name = request.form.get('food')
    expiration = request.form.get('expiration_date')
    quantity = request.form.get('quantity')

    # create a new food item
    new_food = Food(name=name, quantity=quantity, expiration_date=expiration,
        id_user=current_user.id)

    # add the new user to the database
    db.session.add(new_food)
    db.session.commit()

    return redirect(url_for('main.profile'))