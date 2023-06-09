from fastapi import FastAPI, HTTPException
from model import Todo
from fastapi.middleware.cors import CORSMiddleware

from database import(
    fetch_all_todos,
    fetch_one_todo,
    create_todo,
    remove_todo,
    patch_todo
)

app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

@app.get("/")
async def read_root():
    return {"Hello": "Ahosan"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{id}", response_model=Todo)
async def get_todo_by_id(id):
    response = await fetch_one_todo(id)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with {id}")

@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.patch("/api/todo/update/{id}/", response_model=Todo)
async def update_todo(id: int, todo: Todo):
    response = await patch_todo(id, todo)
    return response

@app.delete("/api/todo/{id}")
async def delete_todo(id):
    response = await remove_todo(id)
    if response:
        return "Successfully deleted Todo"
    raise HTTPException(404, f"There is no todo with the id {id}")
