from pydantic import BaseModel
from datetime import datetime


class Plans(BaseModel):
    id_plan: int
    title: str
    plan_description: str
    objetive: str

class PlanAssigment(BaseModel):
    plan_id: int

class Food(BaseModel):
    id: int
    name: str
    description: str
    price: float
    created_at: datetime

class Users(BaseModel):
    id: int
    name: str
    id_plan: int