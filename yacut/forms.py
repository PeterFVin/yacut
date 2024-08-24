from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class YacutForm(FlaskForm):
    original_link = URLField(
        'Введите полную ссылку',
        validators=[DataRequired(message='Это обязательное поле!'),
                    URL(require_tld=True,
                        message='Введите корректную ссылку!')]
    )
    custom_id = URLField(
        'Введите короткую ссылку',
        validators=[
            Length(1, 16,
                   message='Введите ссылку не длиннее 16 символов!'),
            Optional(),
        ]
    )
    submit = SubmitField('Создать')
