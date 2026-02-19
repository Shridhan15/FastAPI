from fastapi import FastAPI, Path, HTTPException, Query
import json

app= FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data=json.load(f)
    return data
 

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