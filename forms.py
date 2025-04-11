from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, StringField, PasswordField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, ValidationError

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
    user_type = SelectField('Account Type', choices=[
        ('client', 'Client'), 
        ('artist', 'Makeup Artist')
    ], validators=[DataRequired()])
    specialization = StringField('Specialization')
    skin_type = StringField('Skin Type')

    def validate_user_type(self, field):
        if field.data not in ['client', 'artist']:
            raise ValidationError("Invalid account type")

    def validate(self, extra_validators=None):
        # Add conditional validation
        if not super().validate():
            return False

        if self.user_type.data == 'artist' and not self.specialization.data:
            self.specialization.errors.append('Specialization is required for artists')
            return False

        if self.user_type.data == 'client' and not self.skin_type.data:
            self.skin_type.errors.append('Skin type is required for clients')
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


    #Make Portfolio Form 
    #Make Publish Events Detail Form 
    #Make 