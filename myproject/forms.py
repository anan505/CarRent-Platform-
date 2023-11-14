from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField

    
class CompanyForm(FlaskForm):
    name = StringField('Company name', validators=[DataRequired()])
    st = SelectField('State', choices=[], coerce=int)
    city = StringField('City', validators=[DataRequired()])
    ISIN = StringField('ISIN', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class ClientForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    DOB = DateField('Date of birth (YYYY-MM-DD)',format='%Y-%m-%d')
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class loginClientForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class loginCompanyForm(FlaskForm):
    ISIN = StringField('ISIN', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class selectTime(FlaskForm):
    start_date = DateField('start at (YYYY-MM-DD)',format='%Y-%m-%d')
    end_date = DateField('end at (YYYY-MM-DD)',format='%Y-%m-%d')
    submit = SubmitField('submit')

class addCarForm(FlaskForm):
    v_id = StringField('license plate number', validators=[DataRequired()])
    brand = StringField('vehicle brand', validators=[DataRequired()])
    model = StringField('vehicle model', validators=[DataRequired()])
    year = SelectField('year', choices=[], coerce=int)
    price = DecimalField('price per day',places = 2)
    seat_num = IntegerField('seats number', validators=[DataRequired()])
    submit = SubmitField('submit')

class addTruckForm(FlaskForm):
    v_id = StringField('license plate number', validators=[DataRequired()])
    brand = StringField('vehicle brand', validators=[DataRequired()])
    model = StringField('vehicle model', validators=[DataRequired()])
    year = SelectField('year', choices=[], coerce=int)
    price = DecimalField('price per day',places = 2)
    load_capacity = IntegerField('load capacity (KG)', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class updateForm(FlaskForm):
    feature = SelectField('State', choices=[], coerce=int)
    value = StringField('Update to', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class searchForm(FlaskForm):
    question = SelectField('Frequently asked question', choices=[], coerce=int)
    submit = SubmitField('search')