from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app_files.models import User

country_choices = [("au", "Australia"), ("br", "Brazil"), ("ca", "Canada"), ("cn", "China"), ("de", "Germany"), 
                   ("eg", "Egypt"), ("fr", "France"), ("gb", "United Kingdom"), ("gr", "Greece"), ("hk", "Hong Kong"), 
                   ("ie", "Ireland"), ("il", "Israel"), ("in", "India"), ("it", "Italy"), ("jp", "Japan"), ("nl", "Netherlands"), 
                   ("no", "Norway"), ("ph", "Phillipines"), ("pt", "Portugal"), ("ro", "Romania"), ("ru", "Russia"), 
                   ("sg", "Singapore"), ("tw", "Taiwan"), ("ua", "Ukraine"), ("us", "USA"), ("ch", "Switzerland")]

lang_choices = [("ar", "Arabic"), ("zh", "Chinese"), ("nl", "Dutch"), ("en", "English"), ("es", "Spanish"), ("hi", "Hindi"),
                ("fr", "French"), ("de", "German"), ("el", "Greek"), ("he", "Hebrew"), ("it", "Italian"), ("ja", "Japanese"),
                ("ml", "Malayalam"), ("mr", "Marathi"), ("no", "Norwegian"), ("pt", "Portuguese"), ("ro", "Romanian"),
                ("ru", "Russian"), ("sv", "Swedish"), ("ta", "Tamil"), ("te", "Telugu"), ("uk", "Ukrainian")]

class RegisterForm(FlaskForm):
    def validate_username(self, uname_to_check):
        user = User.query.filter_by(username=uname_to_check.data).first()
        if user:
            raise ValidationError('Username Exists already! Try with another username')
        
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('This e-Mail Exists already! Try with another e-Mail')
            
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='e-Mail Address: ', validators=[Email(), DataRequired()])
    country = SelectField(label='Country', choices= country_choices, validators=[DataRequired()])
    language = SelectField(label='Language', choices= lang_choices, validators=[DataRequired()])
    pwd1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    pwd2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('pwd1'), DataRequired()])

    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Enter Password: ', validators=[Length(min=6), DataRequired()])

    submit = SubmitField(label='Sign In')

class UpdateLanguageForm(FlaskForm):
    language = SelectField(label='Language', choices= lang_choices)
    submit = SubmitField(label='Apply Changes')

class UpdateCountryForm(FlaskForm):
    country = SelectField(label='Country', choices= country_choices)
    submit = SubmitField(label='Apply Changes')