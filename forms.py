from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField, DecimalField

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')


class NewCustomerForm(FlaskForm):
    GivenName = StringField('GivenName', validators=[validators.DataRequired()])
    Surname = StringField('Surname', validators=[validators.DataRequired()])
    Streetaddress = StringField('Streetaddress', validators=[validators.DataRequired()])
    City = StringField('City', validators=[validators.DataRequired()])
    Zipcode = IntegerField('Zipcode', validators=[validators.DataRequired()])
    Country = StringField('Country', validators=[validators.DataRequired()])
    CountryCode = StringField('CountryCode', validators=[validators.DataRequired()])
    Birthday= DateField('Birthday', validators=[validators.DataRequired()])
    NationalId = IntegerField('NationalId', validators=[validators.DataRequired()])
    TelephoneCountryCode = SelectField('TelephoneCountryCode',choices=[('46','+46'),('41','+41'),('42','+42')])
    Telephone = IntegerField('Telephone', validators=[validators.DataRequired()])
    EmailAddress = StringField('EmailAddress', validators=[validators.DataRequired(), emailContains])

class Depositform(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=1000000)])

class Withdrawform(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=1000000)])

class Transferform(FlaskForm):
    Amount = IntegerField('Amount', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=1000000)])
    Id = IntegerField('Id', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=1000000)])