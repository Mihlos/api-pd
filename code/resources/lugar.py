from flask_restful import Resource, reqparse

from models.lugar import PlaceModel


class Place(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Field "name" is required and must be a string.')

    def get(self, name):
        place = PlaceModel.find_by_name(name)
        if place:
            return place.json()
        return {'message': 'Place not found.'}, 404

    def post(self, name):
        place = PlaceModel(name)
        if PlaceModel.find_by_name(name):
            return {'message': 'Place {} already exists'.format(name)}, 400

        try:
            place.save_to_db()
        except:
            return {'message': 'An error occurred inserting the place.'}, 500

        return place.json(), 201

    def put(self, name):
        place = PlaceModel.find_by_name(name)
        data = Place.parser.parse_args()

        if place is None:
            place = PlaceModel(name)
        else:
            if PlaceModel.find_by_name(data['name']):
                return {'message': 'Place {} already exists.'.format(data['name'])}, 400
            place.name = data['name']

        place.save_to_db()
        return place.json()

    def delete(self, name):
        place = PlaceModel.find_by_name(name)
        if place:
            place.delete_from_db()
            return {'message': 'Place {} deleted'.format(name)}
        return {'message': 'Place not found.'}, 404


class PlaceList(Resource):
    def get(self):
        return [place.json() for place in PlaceModel.query.all()]
