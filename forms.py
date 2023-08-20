from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField, FileField, Label, HiddenField, \
    PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from .models import *


# noinspection PyMethodMayBeStatic
class EditUserForm(FlaskForm):
    user_name = StringField(u'Username',
                            validators=[DataRequired(message='username is required'),
                                        Length(min=1, max=16, message='the length of username must be between 1 and 16'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='username must be composed of letters, numbers and underscores')],
                            render_kw={'placeholder': 'the length of username must be between 1 and 16'})
    nickname = StringField(u'Nickname',
                           validators=[DataRequired(message='nickname is required'),
                                       Length(min=1, max=20, message='the length of nickname must be between 1 and 20')],
                           render_kw={'placeholder': 'the length of nickname must be between 1 and 20'})
    user_email = StringField(u'Email',
                             render_kw={'placeholder': 'email is required', 'type': 'email'})

    submit = SubmitField(u'Register', render_kw={'class': 'btn btn-success btn-xs'})

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user_email.label = Label(self.user_email.id, 'Current Email')
        self.user_email.render_kw = {'disabled': 'true', 'label': 'Current Email'}
        self.submit.label = Label(self.submit.id, 'Save')

    def validate_username(self, filed):
        if filed.data != current_user.username and User.query.filter_by(username=filed.data).first():
            raise ValidationError('the username is already in use!')

    def validate_nickname(self, filed):
        if filed.data != current_user.nickname and User.query.filter_by(nickname=filed.data).first():
            raise ValidationError('the nickname is already in use!')


# noinspection PyMethodMayBeStatic
class RegisterForm(FlaskForm):
    user_name = StringField(u'Username',
                            validators=[DataRequired(message='username is required'),
                                        Length(min=1, max=16, message='the length of username must be between 1 and 16'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='username must be composed of letters, numbers and underscores')],
                            render_kw={'placeholder': 'the length of username must be between 1 and 16'})
    nickname = StringField(u'Nickname',
                           validators=[DataRequired(message='nickname is required'),
                                       Length(min=1, max=20, message='the length of nickname must be between 1 and 20')],
                           render_kw={'placeholder': 'the length of nickname must be between 1 and 20'})
    user_email = StringField(u'Email',
                             validators=[DataRequired(message='email is required'),
                                         Length(min=4, message='the length of email must be greater than 4')],
                             render_kw={'placeholder': 'email is required', 'type': 'email'})
    password = StringField(u'Password',
                           validators=[DataRequired(message='password is required'),
                                       Length(min=8, max=40, message='the length of password must be between 8 and 40'),
                                       EqualTo('confirm_pwd', message='password must be equal to confirm password')],
                           render_kw={'placeholder': 'password is required', 'type': 'password'})
    confirm_pwd = StringField(u'Confirm Password',
                              validators=[DataRequired(message='confirm password is required'),
                                          Length(min=8, max=40, message='password must be between 8 and 40')],
                              render_kw={'placeholder': 'confirm password is required', 'type': 'password'})
    submit = SubmitField(u'Register', render_kw={'class': 'source-button btn btn-primary btn-xs mt-2'})

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate_user_name(self, filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('the username is already in use!')

    def validate_user_email(self, filed):
        if User.query.filter_by(email=filed.data.lower()).first():
            raise ValidationError('the email is already in use!')

    def validate_nickname(self, filed):
        if User.query.filter_by(nickname=filed.data).first():
            raise ValidationError('the nickname is already in use!')


class LoginForm(FlaskForm):
    usr_email = StringField(u'Email/Username', validators=[DataRequired(message='the email or username is required')],
                            render_kw={'placeholder': 'the email or username is required'})
    password = StringField(u'Password',
                           validators=[DataRequired(message='the password is required'),
                                       Length(min=8, max=40, message='the length of password must be between 8 and 40')],
                           render_kw={'type': 'password', 'placeholder': 'password is required'})
    remember_me = BooleanField(u'Remember Me', default=False)
    submit = SubmitField(u'Login', render_kw={'class': 'source-button btn btn-primary btn-xs'})


class BasePostForm(FlaskForm):
    title = StringField(u'Title', validators=[DataRequired(message='the title is required'),
                                           Length(min=1, max=50, message='the length of title must be between 1 and 50')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': 'the length of title must be between 1 and 50'})
    category = SelectField(label=u'Category',
                           default=0,
                           coerce=int)
    body = CKEditorField('Context', validators=[DataRequired(message='Content is required')])
    submit = SubmitField(u'Publish', render_kw={'class': 'source-button btn btn-primary btn-xs mt-2 text-right'})

    def __init__(self, *args, **kwargs):
        super(BasePostForm, self).__init__(*args, **kwargs)
        categories = PostCategory.query.all()
        self.category.choices = [(cate.id, cate.name) for cate in categories]


# noinspection PyMethodMayBeStatic
class CreatePostForm(BasePostForm):

    def validate_title(self, filed):
        if Post.query.filter_by(title=filed.data).first():
            raise ValidationError('the title is already in use!')


class EditPostForm(BasePostForm):
    submit = SubmitField(u'Save', render_kw={'class': 'source-button btn btn-danger btn-xs mt-2 text-right'})


class UploadAvatarForm(FlaskForm):
    image = FileField('Avator', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'format must be jpg or png')
    ])
    submit = SubmitField(u'Upload', render_kw={'class': 'btn btn-success'})


class CropAvatarForm(FlaskForm):
    x = HiddenField(u'', render_kw={'hidden': 'hidden'})
    y = HiddenField(u'', render_kw={'hidden': 'hidden'})
    w = HiddenField(u'', render_kw={'hidden': 'hidden'})
    h = HiddenField(u'', render_kw={'hidden': 'hidden'})
    submit = SubmitField(u'Modify Avator', render_kw={'class': 'btn btn-success'})


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old Password', validators=[DataRequired()])
    password = PasswordField('new Password', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('confirm', validators=[DataRequired()])
    set = SubmitField(u'Modify', render_kw={'class': 'btn btn-success'})
