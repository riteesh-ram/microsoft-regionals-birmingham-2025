from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import HiddenField, FileField, SubmitField

# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Optional




class AdmissionForm(FlaskForm):
    title = SelectField(
        "Title",
        choices=[
            ("", "-- Select Title --"),
            ("Mr", "Mr"),
            ("Mrs", "Mrs"),
            ("Ms", "Ms"),
            ("Miss", "Miss"),
            ("Dr", "Dr")
        ],
        validators=[Optional()]
    )
    other_title = StringField("Other Title", validators=[Optional()])
    forename = StringField("Forename", validators=[DataRequired()])
    middle_name = StringField("Middle Name", validators=[Optional()])
    surname = StringField("Surname", validators=[DataRequired()])

    flat_number = StringField("Flat Number", validators=[Optional()])
    building_name = StringField("Building Name", validators=[Optional()])
    house_number_name = StringField("House Number/Name", validators=[DataRequired()])
    district = StringField("District", validators=[Optional()])
    street = StringField("Street", validators=[DataRequired()])
    town = StringField("Town", validators=[DataRequired()])
    county = StringField("County", validators=[DataRequired()])
    post_code = StringField("Post Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])

    home_phone = StringField("Home Phone", validators=[Optional()])
    work_phone = StringField("Work Phone", validators=[Optional()])
    mobile_phone = StringField("Mobile Phone", validators=[DataRequired()])
    email_address = StringField("Email", validators=[Optional(), Email()])
    contact_notes = TextAreaField(
        "Alternative Contact Notes",
        validators=[Optional(), Length(max=200)]
    )
    preferred_communication = SelectField(
        "Preferred Communication",
        choices=[
            ("", "-- Select One --"),
            ("Phone", "Phone"),
            ("Email", "Email"),
            ("Mail", "Mail")
        ],
        validators=[DataRequired()]
    )
class BlueBadgeForm(FlaskForm):
    fullName = StringField("Full Name", validators=[DataRequired()])
    niNumber = StringField("National Insurance Number", validators=[DataRequired()])
    addressLine1 = StringField("Address Line 1", validators=[DataRequired()])
    addressLine2 = StringField("Address Line 2", validators=[Optional()])
    postCode = StringField("Postcode", validators=[DataRequired()])
    mobilityAid = StringField("Mobility Aid", validators=[Optional()])
    mobilityIssues = TextAreaField("Mobility Issues", validators=[Optional()])
    phone = StringField("Phone Number", validators=[Optional()])
    email = StringField("Email Address", validators=[Optional(), Email()])
    submit = SubmitField("Apply")

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    # We don't need a SubmitField because that won't let us use an icon for the button
    # Instead we just put a HTML button element with type="submit", and the icon in the
    # body of the element. That is all we need to submit the form. Note that we don't care
    # what the value or name of the button is.

class FileUploadTXTForm(FlaskForm):
    file = FileField('Upload a Text File', validators=[FileRequired(), FileAllowed(['txt'])])
    submit = SubmitField('Upload')

class FileUploadCSVForm(FlaskForm):
    file = FileField('Upload a CSV File', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')

class TextInputForm(FlaskForm):
    text_input = StringField("Text Input", validators=[DataRequired()])
