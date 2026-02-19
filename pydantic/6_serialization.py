from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin:str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address_dict= {'city':'a', "state":'b', 'pin':'1212'}
address1= Address(**address_dict)
patient_dict= {'name':'ram','gender':'male','age':34,'address':address1}
patient1= Patient(**patient_dict)
print(patient1)
print(patient1.address.pin)


temp=patient1.model_dump()
# temp=patient1.model_dump( include=['name']) # export name only
# temp=patient1.model_dump( exclude={'address':['state']}) # export excepty state from address
# temp=patient1.model_dump(exclude_unset= true) # do not send unset values 
temp2=patient1.model_dump_json()
print("Temp", temp)
print(type(temp))