from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField
from wtforms.validators import InputRequired
from datetime import date

# Food form

class FoodForm(FlaskForm):
    food_name = StringField(
        'Food name',
        id='food_name',
        validators=[InputRequired()]
    )

    quantity = DecimalField(
        'Quantity',
        id='quantity',
        validators=[InputRequired()]
    )

    expiration_date = DateField(
        'Expiration date',
        id='expiration_date',
        default=date.today,
        validators=[InputRequired()]
    )

    def validate_on_submit(self):
        result = super(FoodForm, self).validate()
        print(self.food_name.data, self.expiration_date.data, self.quantity.data)
        if not result:
            return False
            
        if self.expiration_date.data < date.today() or self.quantity.data <= 0:
            return False
        else:
            return result