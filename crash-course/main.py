#first importing   the things we need the most 
from fastapi import FastAPI
from typing import Optional , List 
from enum import IntEnum
from pydantic import BaseModel , Field

#we are going to create an app using fast api
app = FastAPI()

#after defining the application app()
#we need to define the schema


#using enum  i will set the priority  - which we are going to use as a  part of todo
class Priority (IntEnum):
    LOW  = 3 
    MEDIUM = 2
    HIGH = 1

#using pydantic to create a schema to define the functionality - its is done using pydantic space model

class TodoBase(BaseModel):
    '''
    the thing about description is - it is majorly about documentation
    but if it comes to be integrated with open ai model then the model will see this as the context
    '''
    todo_name : str = Field(..., min_length=3 , max_length=512 , description = "Name of the todo")
    todo_description : str = Field(..., min_length=5 , description = "Description of the todo")
    #so the priority of the todo is the instance of the class Priority
    todo_priority : Priority  = Field(default =  Priority.LOW , description = "Priority of the todo")



#creating a model for creating a todo - different models for different end points
class TodoCreate(TodoBase):
    pass


'''
#creating a type of the TODO - since i am inherinting  the todobase class here the Todo will have the propperty of Todo_name and Todo_description - and so 
#if i want to set the response type to be Todo classs then it will havbe alll the threee property 
'''
class Todo(TodoBase):
    todo_id : int = Field(..., description = "unique ID of the todo") #this is going to be used for creating a todo





#class(schema) for updating the Todo - why i am making it from BaseModel beacuse its going to be like the todo base but its going to be optional for a bunch for a bunch of fields
class TodoUpdate(BaseModel ):
    todo_name : Optional[str] = Field(None, min_length=3 , max_length=512 , description = "Name of the todo")
    todo_description :  Optional[str] = Field(None, min_length=5 , description = "Description of the todo")
    #so the priority of the todo is the instance of the class Priority
    todo_priority : Optional[Priority]  = Field(None , description = "Priority of the todo")




#lets create a in memory database - list of dictionries 
all_todos = [
    Todo(todo_id=1, todo_name="Clean house", todo_description="Cleaning the house thoroughly", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Sports", todo_description="Going to the gym for workout", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Read", todo_description="Read chapter 5 of the book", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Work", todo_description="Complete project documentation", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Study", todo_description="Prepare for upcoming exam", priority=Priority.LOW)
]




#creating endpoints
#GET , PUT , POST , DELETE

#creating a get endpoint 
#asynchronous function which will anyhow do a job that will take time - for eg getting data from database
@app.get("/data")
async def get_data_fromdb():
    #we will need to use await here
    pass
    return ""




#handling the todos here

#get request 

#to get a single todo 
#using path parameters - #localhost:9999/todos/2
@app.get("/todo/{todo_id}" , response_model=Todo)
def get_todo(todo_id:int):
    print("running")
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo


#using query parameter
#localhost:9999/todos?first_n=3 - to build this we dont give it in the url but we give it in the function 
@app.get('/todos')
def get_todos(first_n:Optional[int] = 0):
    if first_n is None:
        return all_todos
    elif first_n is not None and  first_n > 0 and first_n<= 5:
        first_n_todos = all_todos[:first_n] 
        return first_n_todos
    else:
        return {"please input something valid under 1-5"}
    


#post endpoint

#endpoint to add todo
@app.post("/todos")
def add_todo(todo:dict):
    # first we get the ids lst

    ##simpler approach - 
    id = []
    for todo in all_todos:
        id.append(todo['todo_id'])

    #now since we have the list of all the todo_id we can find the max in them and then we can add 1 and asssign it as the new todo id
    new_todo_id = max(id)+1


    #better approach to  build the new todo - as for bigger data set this approach will fall out

    #“For every todo in the list all_todos, give me the value of its 'todo_id' key.”
    new_todo_id_better_approach = max(todo['todo_id'] for todo in all_todos) + 1

    #creating new todo 
    new_todo ={
        "todo_id": new_todo_id_better_approach,
        "todo_name": todo["todo_name"],
        "todo_description": todo["todo_description"]
    }


    all_todos.append(new_todo)
    return new_todo



#update endpoint - put 
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, updated_todo:dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            todo["todo_name"] = updated_todo['todo_name']
            todo['todo_description'] = updated_todo['todo_description']
            return todo
        
    return "error,todo not found"


#delete endpoint  - using delete
@app.delete("/todos/{todo_id}")
def delet_todo(todo_id:int):
    for index , todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            todo_deleted = all_todos.pop(index)
            return todo_deleted
    return "todo not found ! so we cant delete anything " 
