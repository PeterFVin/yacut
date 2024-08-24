from http import HTTPStatus as status
from re import match

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def index_view_api():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not data.get('custom_id'):
        data.update({"custom_id": get_unique_short_id()})
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')
    if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), status.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def redirect_url_api(short):
    redirect = URLMap.query.filter_by(short=short).first()
    if not redirect:
        raise InvalidAPIUsage('Указанный id не найден', status.NOT_FOUND)
    return jsonify({'url': redirect.original}), status.OK
