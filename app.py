from flask_jwt import JWT, jwt_required
from flask import Flask, request
from flask_restful import Resource, Api
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

items = []


class Saludo(Resource):

    @jwt_required()
    def get(self, name):
        """
        filter busca name en items, creamos una lista con ese dato y buscaamos el siguiente, sino existe devolvemos None
        :param name: nombre del elemento a introducir
        :return: item buscado si es None no existe
        """
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    # data = request.get_json(force=True) force=True means that you no need content header
    # data = request.get_json(silent=True) silent=True is doesn't give error return none

    def post(self, name):
        """
        item = {'name': name, 'price': 12.00}
        :param name:
        :return:
        """
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


api.add_resource(Saludo, '/saludo/<string:name>')
app.run()
