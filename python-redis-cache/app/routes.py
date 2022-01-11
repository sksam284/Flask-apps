# search_app/routes.py
from app import views
from flask_restful import Api
from . import app

api = Api(app, prefix="/api")

api.add_resource(views.MasterDataApi, '/master-data/<string:data_key>', methods=['GET', 'PATCH', 'DELETE'],
                 endpoint='master-data')
api.add_resource(views.MasterDataCreateApi, '/master-data/', methods=['GET', 'POST'],
                 endpoint='master-data-create')
