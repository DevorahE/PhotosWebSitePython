from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, RadioField


class CreatePictureForm(FlaskForm):
    file = FileField(label='Your picture')
    options = RadioField(label="Option", choices=[('color', 'Change the color'), ('border', 'Add a border'), ('identify', 'Identify a figure')])
    submit = SubmitField(label='Submit')

