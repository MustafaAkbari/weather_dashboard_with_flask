from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class WeatherForm(FlaskForm):
    city_name = StringField("City Name:", validators=[DataRequired()], render_kw={"placeholder": "City Name"})
    submit = SubmitField("Get Weather Info")
