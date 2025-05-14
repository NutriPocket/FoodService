from pydantic import BaseModel
from datetime import datetime


class Plans(BaseModel):
    id_plan: int
    title: str
    plan_description: str
    objetive: str

class FoodPlanLink(BaseModel):
    food_id: int
    plan_id: int

class Food(BaseModel):
    id: int
    name: str
    description: str
    price: float
    created_at: datetime