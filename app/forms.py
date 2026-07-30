from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    phone = StringField("Your Phone", validators=[Optional(), Length(max=20)])
    message = TextAreaField("Your Message", validators=[DataRequired(), Length(max=2000)])


class VolunteerForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    phone = StringField("Your Phone", validators=[DataRequired(), Length(max=20)])
    interest = SelectField(
        "I'm interested in",
        choices=[
            ("Volunteer", "Volunteering"),
            ("Partner", "NGO Partnership"),
            ("CSR", "CSR Collaboration"),
        ],
        validators=[DataRequired()],
    )
    message = TextAreaField("Tell us more (optional)", validators=[Optional(), Length(max=1000)])


class NewsletterForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")


class CampaignForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    pillar = SelectField(
        "Pillar",
        choices=[
            ("Environment", "Environment"),
            ("Mental Health", "Mental Health"),
            ("Skill Development", "Skill Development"),
        ],
        validators=[DataRequired()],
    )
    summary = StringField("Short Summary", validators=[DataRequired(), Length(max=300)])
    description = TextAreaField("Full Description", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[Optional(), Length(max=300)])
    is_active = BooleanField("Active", default=True)
    is_featured = BooleanField("Featured on homepage", default=False)