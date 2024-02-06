from todos import app, api
from todos.endpoints.todo import ns as todo_namespace
from todos.endpoints.user import ns as user_namespace


api.add_namespace(todo_namespace)
api.add_namespace(user_namespace)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
