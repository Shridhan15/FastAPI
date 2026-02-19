
from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict,Optional, Annotated


class Patient(BaseModel):
    name:str
    age:int 
    email:EmailStr
    linkedin_url: AnyUrl
    weight:float
    married:bool
    allergies:list[str]
    contact_details: dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age >60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients older than 60 must have emergency contact")
    
        return model



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("Patient data inserted successfully")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
   
    print("Patient data updated successfully")



patient_info={'name': "John Doe", 'age': '90','email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com',  'weight': "70.5", 'married': True, 'allergies':['abc'] ,  'contact_details': {'email': 'john.doe@example.com', 'phone': '123-456-7890', 'emergency':'12331'}} # age is a string instead of an integer, but Pydantic will handle the type conversion and validation

patient1= Patient(**patient_info) 
insert_patient_data(patient1)