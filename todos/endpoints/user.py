from todos import api
from flask_restx import Resource, Namespace, fields


ns = Namespace("users", path="/users", description="Users Api")


users = []

create_users_api_model = ns.model(
    "createUserPayload",
    {"name": fields.String(required=True, description="User details payload")},
)

create_users_api_response = ns.model(
    "createUserResponse",
    {"name": fields.String(required=True, description="User details response")},
)


@ns.route("/")
class Users(Resource):
    @ns.marshal_list_with(create_users_api_response)
    def get(self):
        return users

    @ns.expect(create_users_api_model)
    def post(self):
        newUser = ns.payload
        newId = 1 if len(users) == 0 else 1 + max([x["id"] for x in users])
        users.append({"id": newId, "name": newUser["name"]})
        return users


@ns.route("/<int:id>")
class User(Resource):
    @ns.marshal_with(create_users_api_response)
    def get(self, id):
        users_list = [user for user in users if user["id"] == id]
        if len(users_list) > 0:
            return users_list[0]
        ns.abort(404, f"User with id {id} does not exist")

    @ns.expect(create_users_api_model)
    @ns.marshal_with(create_users_api_response)
    def put(self, id):
        user_ids = [user["id"] for user in users]
        if id not in user_ids:
            ns.abort(404, f"User with id {id} does not exist")
        user_index = [user["id"] for user in users].index(id)
        users[user_index]["task"] = ns.payload["name"]
        return users[user_index]
