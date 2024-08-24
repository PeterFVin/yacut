from re import match

from flask import flash, redirect, render_template, request

from yacut import app, db
from yacut.forms import YacutForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            form.custom_id.errors = [('Предложенный вариант короткой '
                                      'ссылки уже существует.')]
            return render_template('yacut.html', form=form)
        if not match(r'^[A-Za-z0-9]{1,16}$', custom_id):
            form.custom_id.errors = [('Указано недопустимое имя '
                                      'для короткой ссылки')]
            return render_template('yacut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        flash(f'Ваша новая ссылка: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('yacut.html', form=form)

@app.route('/<string:short>', methods=['GET'])
def redirect_url(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
