from fastapi import FastAPI
from pydantic import BaseModel
from typing import List 


app = FastAPI()

class Tea(BaseModel):
   id: int
   nane:str
   origin:str

teas:List[Tea]= [] ## creating a list named teas which will be an array of Tea objects

@app.get("/")
def read_root():
   return {
      "message": " ajao bhai"
   }

@app.get("/teas")
def get_teas():
   return teas 


##doing the post request
@app.post("/teas")
def add_teas(tea: Tea):
   teas.append(tea)
   return {
      "msg" : "teas were added successfully"
   }

##doing a put method 
@app.put("/tea/{tea_id}")
def update_tead(tea_id:int , updated_tea:Tea): ##passsing the tea_id as  whatever we are taking we need to pass it as parameter as the name is \
   for index, tea in enumerate(teas):
      if tea.id == tea_id:
         teas[index] = updated_tea
         return {
            "msg": "Tea updated successfully"
         }
      
      return {" msg": "Tea not found" }
   



##using delete method
@app.delete("/tea/{tea_id}")
def delete_tea(tea_id:int):
   for index , tea in enumerate(teas):
      if teas.id == tea_id:
         deleted = teas.pop(index)
         return {
                "msg": "Tea deleted successfully",
                "deleted_tea": deleted 
            }
      return {"tea not found "}
   