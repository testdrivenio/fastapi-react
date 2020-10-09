from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
        CORSMiddleware, 
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

todos = [
    {
        "id": 1,
        "item": "Read a book."
    },
    {
        "id": 2,
        "item": "Cycle around town."
    }
]

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your to-do list."}

@app.get("/todo", tags=["To-dos"])
async def get_todos() -> dict:
    return {
        "data": todos
    }

@app.post("/todo", tags=["To-dos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": {
            "To-do added."
        }
    }

@app.put("/todo/{id}", tags=["To-dos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if todo['id'] == id:
            todo['item'] = body['item']

    return {
        "data": "Todo with id {} has been updated.".format(id)
    }

@app.delete("/todo/{id}", tags=["To-dos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if todo['id'] == id:
            todos.remove(todo)
    return {
        "data": "To-do with id {} removed.".format(id)
    }
