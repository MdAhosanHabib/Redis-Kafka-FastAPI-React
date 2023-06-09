import mysql.connector
from model import Todo
from fastapi import HTTPException
import redis
import json
from model import TodoResponse
from pydantic import ValidationError
from kafka import KafkaProducer, KafkaConsumer

redis_client = redis.Redis(host='192.168.222.128', port=6379)

mysql_connection = mysql.connector.connect(
    host="192.168.222.128",
    user="TodoList",
    password="Todo_List123",
    database="TodoList"
)
mysql_cursor = mysql_connection.cursor()

async def fetch_one_todo(id):
    item_data = redis_client.get(id)
    if item_data:
        item_data = json.loads(item_data.decode())
        try:
            todo_response = TodoResponse(item_id=id, **item_data)
            return todo_response
        except ValidationError as e:
            raise HTTPException(status_code=500, detail="Incomplete data in Redis cache")
    try:
        query = "SELECT * FROM TodoList.todo WHERE id = %s"
        mysql_cursor.execute(query, (id,))
        result = mysql_cursor.fetchone()
        if result:
            item_data = {
                "id": result[0],
                "name": result[1],
                "address": result[2],
                "phone": result[3]
            }
            redis_client.set(id, json.dumps(item_data))
            todo_response = TodoResponse(**item_data)
            return todo_response
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_all_todos():
    todos_data = redis_client.get("todos")
    if todos_data:
        todos = json.loads(todos_data.decode())
        return {"data": todos}
    try:
        query = "SELECT * FROM TodoList.todo"
        mysql_cursor.execute(query)
        results = mysql_cursor.fetchall()
        todos = []
        for result in results:
            item = {
                "id": result[0],
                "name": result[1],
                "address": result[2],
                "phone": result[3]
            }
            todos.append(item)
        redis_client.set("todos", json.dumps(todos))
        return {"data": todos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_todo(todo):
    try:
        #Serialize item data
        item_data = json.dumps(todo)
        producer = KafkaProducer(bootstrap_servers='ahosan1rnd:9092')
        producer.send('testTopic', value=item_data.encode())
        producer.close()
        #Flush Redis cache
        redis_client.flushall()
        item = {
            "name": todo["name"],
            "address": todo["address"],
            "phone": todo["phone"]
        }
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    ##---if do not use kafka---##
    #query = "INSERT INTO TodoList.todo (name, address, phone) VALUES (%s, %s, %s)"
    #values = (todo["name"], todo["address"], todo["phone"])
    #mysql_cursor.execute(query, values)
    #mysql_connection.commit()
    ##Flush Redis cache
    #redis_client.flushall()
    #item = {
    #        "name": todo["name"],
    #        "address": todo["address"],
    #        "phone": todo["phone"]
    #    }
    #return item

async def remove_todo(id):
    query = "DELETE FROM todo WHERE id = %s"
    values = (id),
    mysql_cursor.execute(query, values)
    mysql_connection.commit()
    #Flush Redis cache
    redis_client.flushall()
    return True

async def patch_todo(id: int, todo: Todo):
    #Flush Redis cache
    redis_client.flushall()
    select_query = "SELECT * FROM TodoList.todo WHERE id = %s"
    select_values = (id,)
    mysql_cursor.execute(select_query, select_values)
    existing_todo = mysql_cursor.fetchone()

    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    #Convert the tuple to a dictionary
    existing_todo_dict = dict(zip(mysql_cursor.column_names, existing_todo))
    #Apply partial updates to the existing todo
    updated_todo_dict = {**existing_todo_dict, **todo.dict(exclude_unset=True)}
    #Update the todo item in the database
    update_query = "UPDATE TodoList.todo SET name = %s, address = %s, phone = %s WHERE id = %s"
    update_values = (updated_todo_dict['name'], updated_todo_dict['address'], updated_todo_dict['phone'], id)
    mysql_cursor.execute(update_query, update_values)
    mysql_connection.commit()
    return Todo(**updated_todo_dict)
