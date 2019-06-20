from flask_restful import Resource

from models.lugar import PlaceModel


class Place(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help='Field "id" must be a integer.')
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='Field "name" must be a string.')
    '''
    def get(self, name):
        place = PlaceModel.find_by_name(name)
        if place:
            return place.json()
        return {'message': 'Place not found.'}, 404

    def post(self, name):
        '''
        data = Place.parser.parse_args()
        place = PlaceModel(**data)
        '''
        place = PlaceModel(name)
        if PlaceModel.find_by_name(name):
            return {'message': 'Place {} already exists'.format(name)}, 400

        try:
            place.save_to_db()
        except:
            return {'message': 'An error occurred inserting the place.'}, 500

        return place.json(), 201

    def put(self):
        pass

    def delete(self):
        pass


class PlaceList(Resource):
    def get(self):
        return [place.json() for place in PlaceModel.query.all()]
