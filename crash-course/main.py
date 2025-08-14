#first importing fast api
from fastapi import FastAPI
from typing import Optional

#we are going to create an app using fast api
app = FastAPI()



#lets create a in memory database - list of dictionries 
all_todos = [
    {'todo_id': 1, 'todo_name': 'Sports', 'todo_description': 'Go to the gym'},
    {'todo_id': 2, 'todo_name': 'Read', 'todo_description': 'Read 10 pages'},
    {'todo_id': 3, 'todo_name': 'Shop', 'todo_description': 'Go shopping'},
    {'todo_id': 4, 'todo_name': 'Study', 'todo_description': 'Study for exam'},
    {'todo_id': 5, 'todo_name': 'Meditate', 'todo_description': 'Meditate 20 minutes'}
]



#creating endpoints
#GET , PUT , POST , DELETE

#creating a get endpoint 

@app.get("/")
def index():
    return {"message":"hello"}

#so we can apparently define asynchronous and synchronous endpoints here


##let  see the example of the synchronous thing which is bound to take the cpu time
@app.get("/calculation")
def calculation():
    pass
    return ""

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
@app.get("/todo/{todo_id}")
def get_todo(todo_id:int):
    print("running")
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            return {"todo":todo}


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
