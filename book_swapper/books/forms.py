from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


class NewBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    subject_subcategory = StringField('Subject #2', validators=[DataRequired()])
    condition = TextAreaField('Condition', validators=[DataRequired()])
    date_posted = DateField('Date Posted', format='%Y-%m-%d')
    submit = SubmitField('Post')