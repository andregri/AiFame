from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange
from datetime import date

# Food form

class FoodForm(FlaskForm):
    food_name = StringField(
        'Food name',
        id='food_name',
        validators=[DataRequired()]
    )

    quantity = DecimalField(
        'Quantity',
        id='quantity',
        validators=[DataRequired()]
    )

    expiration_date = DateField(
        'Expiration date',
        id='expiration_date',
        default=date.today,
        validators=[DataRequired()]
    )

    def validate_on_submit(self):
        result = super(FoodForm, self).validate()
        if self.expiration_date.data < date.today() and self.quantity.data <= 0:
            return False
        else:
            return result