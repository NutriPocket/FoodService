from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union


class Plans(BaseModel):
    id_plan: int
    title: str
    plan_description: str
    objetive: str

class Plan(BaseModel):
    id_plan: int
    title: str
    plan_description: str
    objetive: str
    weekly_plan: Dict[str, Dict[str, Union[dict, str]]]

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

class FoodPreferenceRequest(BaseModel):
    user_id: str
    preferences: List[str]
