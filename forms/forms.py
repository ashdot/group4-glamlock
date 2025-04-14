from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, FloatField, StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8),
        EqualTo('confirm_password', message="Passwords must match")
    ])
    confirm_password = PasswordField('Confirm Password')
    user_type = SelectField('Account Type', choices=[ #List/array with account type
        ('client', 'Client'), 
        ('artist', 'Makeup Artist') 
    ], validators=[DataRequired()])
    specialization = StringField('Specialization')
    skin_type = StringField('Skin Type')

    def validate_user_type(self, field):
        if field.data not in ['client', 'artist']:
            raise ValidationError("Invalid account type")

    def validate(self, extra_validators=None):
        if not super().validate():
            return False

        # Specialization only required for artists
        if self.user_type.data == 'artist' and not self.specialization.data.strip():
            self.specialization.errors.append('Specialization is required for artists')
            return False

        # Client fields validation
        if self.user_type.data == 'client':
            if not self.phone.data.strip():
                self.phone.errors.append('Phone number is required')
                return False
            if not self.skin_type.data.strip():
                self.skin_type.errors.append('Skin type is required')
                return False

        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class BookingForm(FlaskForm):
    service_type = SelectField('Service Type', 
        choices=[
            ('consultation', 'Consultation'),
            ('bridal', 'Bridal Makeup'),
            ('event', 'Event Makeup')
        ],
        validators=[DataRequired()]
    )
    
    artist_id = SelectField('Artist', 
        coerce=int,
        validators=[DataRequired()]
    )
    
    datetime = DateTimeLocalField(
        'Date & Time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
    
    notes = TextAreaField('Special Requests')

class EditBookingForm(FlaskForm):
    status = SelectField('Status', 
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled')
        ],
        validators=[DataRequired()]
    )
    datetime = DateTimeLocalField(
        'Date & Time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
    notes = TextAreaField('Notes')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Product')

class PortfolioForm(FlaskForm):
    name = StringField('Portfolio Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    image = FileField('Portfolio Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Portfolio')

class PortfolioItemForm(FlaskForm):
    image = FileField('Portfolio Image', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Images only!')
    ])
    description = TextAreaField('Description')
    submit = SubmitField('Add to Portfolio')