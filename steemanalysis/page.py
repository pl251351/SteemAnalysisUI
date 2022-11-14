from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, BooleanField, SelectField, DecimalField
from wtforms.validators import NumberRange


class PageForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    numberofpages = IntegerField('Rows Per Page', validators=[NumberRange(10, 1000, 'number between 10 and 100')])
    submit = SubmitField('Set Page')
    view_all = BooleanField('View all entries')


class AnalysisForm(FlaskForm):
    analyze_for = SelectField('Analyze Data For Sentiment Engine',
                              choices=[('vader', 'Vader'), ('google', 'Google'), ('ibm', 'IBM Watson'), ('tb', 'Text '
                                                                                                               'Blob'), ('flair', 'Flair')])
    drop_bottom = DecimalField('Drop records below quantile', places=4,
                               validators=[NumberRange(0, 1, 'decimal number between 0 and 1')])
    drop_top = DecimalField('Drop records above quantile', places=4,
                            validators=[NumberRange(0, 1, 'decimal number between 0 and 1')])
    use_records_with_value = DecimalField('Only use records where sentiment value is higher than', places=4,
                                          validators=[NumberRange(0, 1, 'decimal number between 0 and 1')])
    drop_zero_value_earned = BooleanField('Drop all where value earned is zero')
    submit = SubmitField('Analyze')
