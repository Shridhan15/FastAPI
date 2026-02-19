from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app= FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data=json.load(f)
    return data
 
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get('/')
def hello():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {"message": "A fully functional API for managing patient records."}

@app.get('/view')
def view_patients():
    data=load_data()
    return data


# path parameter to get patient by id
# with Path and HTTPException for error handling
@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",examples="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")



# query parameter to search patients 
@app.get('/sort')
def sort_patients(sort_by: str= Query(..., description="The field to sort patients by", examples="age"), order: str= Query("asc", description="The order to sort patients (asc or desc)", examples="asc")):
    valid_fields =['height',"weight","bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: asc, desc")
    
    data=load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by])

    if order == "desc":
        sorted_data.reverse()
    return sorted_data



class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="Place of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=80,description="Age of patient")]
    gender: Annotated[Literal['male', 'female','others'], Field(..., description='gender of patient')]
    height: Annotated[float, Field(..., gt=0, description="Height of patient(in m)")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of patient(kgs)")]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi<25:
            return 'normal'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'overweight'
    

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data=load_data()

    # check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")

    # new patient add to DB
    data[patient.id]=patient.model_dump(exclude=['id'])

    # save to json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':"Patient created"})








