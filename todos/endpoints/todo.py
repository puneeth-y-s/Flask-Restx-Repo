from todos import api
from flask_restx import Resource, Namespace, fields
from werkzeug.exceptions import NotFound

ns = Namespace("todos", path="/todos", description="Todo's Api")
parser = ns.parser()

todos = []

create_task_api_model = ns.model(
    "createTaskPayload",
    {"task": fields.String(required=True, description="Todo details payload")},
)

create_task_api_response = ns.model(
    "createTaskResponse",
    {"task": fields.String(required=True, description="Todo details response")},
)

missing_id_model = ns.model("ID_404", {"message": fields.String, "id": fields.Integer})


@ns.route("/")
class Todos(Resource):
    @ns.marshal_list_with(create_task_api_response)
    def get(self):
        """
        get todo's
        """
        return todos

    # @ns.expect(create_task_api_model)
    @ns.doc(body=create_task_api_model)
    def post(self):
        """
        Create a todo
        """
        newTodo = ns.payload
        newId = 1 if len(todos) == 0 else 1 + max([x["id"] for x in todos])
        todos.append({"id": newId, "task": newTodo["task"]})
        return todos


@ns.route("/<int:id>")
class Todo(Resource):
    @ns.marshal_with(create_task_api_response)
    @ns.response(404, "Object Not Found", model=missing_id_model)
    def get(self, id):
        """
        get todo by id
        """
        todos_list = [todo for todo in todos if todo["id"] == id]
        if len(todos_list) > 0:
            return todos_list[0]
        raise NotFound(f"Todo with id {id} does not exist")

    @ns.expect(create_task_api_model)
    @ns.marshal_with(create_task_api_response)
    def put(self, id):
        """
        update a todo by id
        """
        todo_ids = [todo["id"] for todo in todos]
        if id not in todo_ids:
            ns.abort(404, f"Todo with id {id} does not exist")
        todo_index = [todo["id"] for todo in todos].index(id)
        todos[todo_index]["task"] = ns.payload["task"]
        return todos[todo_index]
