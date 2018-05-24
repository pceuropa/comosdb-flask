from flask import Flask
from flask_restplus import Api, Resource, fields
from db import Db

# Extensions initialization
# =========================
app = Flask(__name__)
api = Api(app)
ns = api.namespace('users', description='TODO operations')

user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'email': fields.String(required=True, description='first and last name'),
    'full_name': fields.String(required=True, description='first and last name'),
    'password': fields.String(required=True, description='password')

})

message = api.model('Message', {
    'title': fields.String(required=True, description='title'),
    'content': fields.String(required=True, description='ble'),
    'magic_number': fields.Integer(required=True),
})

db = Db()
db.migrate()


@ns.route('/')
class CreateUser(Resource):

    @ns.doc('get_all_users')
    def get(self):
        return list(db.get_all_users()), 201

    @ns.expect(user)
    @ns.doc('create_user')
    def post(self):
        return db.create_user(api.payload), 201


@ns.route('/<email>')
@ns.doc('delete_user')
class DeleteUser(Resource):

    def delete(self, email):
        return db.create_user(email), 201


@ns.route('/<email>/message')
@ns.doc('create_message')
class Message(Resource):

    def get(self, email):
        return email, 201

    @ns.expect(message)
    def post(self, email):
        return db.create_message(email, api.payload)


@ns.route('/message')
class GetMessage(Resource):

    def get(self):
        return db.get_messages(), 201


if __name__ == '__main__':
    app.run()
