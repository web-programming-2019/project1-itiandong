from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1,20)])
    submit = SubmitField('登录')


class RegisterForm(LoginForm):
    submit = SubmitField('注册')


class SearchForm(FlaskForm):
    isbn = StringField('ISBN', validators=[Length(0,20)])
    title = StringField('书名', validators=[Length(0,200)])
    author = StringField('作者', validators=[Length(0,50)])
    year = StringField('出版年', validators=[Length(0,50)])
    submit = SubmitField('搜索')

class ReviewForm(FlaskForm):
    body = TextAreaField('评论：', validators=[DataRequired(), Length(1, 500)])
    submit = SubmitField()