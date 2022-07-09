from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField,StringField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    text = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdatePostForm(FlaskForm):
    text = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Update Post')

class CommentForm(FlaskForm):
    text = StringField('', validators=[DataRequired()])
    submit = SubmitField('Comment')