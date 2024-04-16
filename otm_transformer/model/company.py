import uuid
from pydantic import BaseModel
from pydantic import BaseModel

class CharacValue(BaseModel):
    id: str = str(uuid.uuid4())
    departmentId: int | None = None
    characId: int
    characValueId: int 
    positiveValue: int
    
class Company(BaseModel):
    id: str
    name: str
    version: str
    sectors: list[int] | None = None
    subSectors: list[int] | None = None
    departmens: list[int] | None = None
    size: int | None = None
    depaCharacValues: list[CharacValue] | None = None
