from flask import Flask
from flask_restful import Api

from resources.lugar import Place, PlaceList

app = Flask('__name__')

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'data_db',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Place, '/v1/place/<string:name>')
api.add_resource(PlaceList, '/v1/places')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8081, debug=True)
