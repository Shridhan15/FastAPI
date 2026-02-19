
from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict,Optional, Annotated


class Patient(BaseModel):
    name:str
    age:int 
    email:EmailStr
    linkedin_url: AnyUrl
    weight:float
    height:float
    married:bool
    allergies:list[str]
    contact_details: dict[str, str]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi=self.weight/ (self.height**2)
        return bmi



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("Patient data inserted successfully")
 

patient_info={'name': "John Doe", 'age': '90','email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com',  'weight': "70.5",'height':1.72 ,'married': True, 'allergies':['abc'] ,  'contact_details': {'email': 'john.doe@example.com', 'phone': '123-456-7890', 'emergency':'12331'}} # age is a string instead of an integer, but Pydantic will handle the type conversion and validation

patient1= Patient(**patient_info) 
insert_patient_data(patient1)