from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from models.foodPlans import FoodPreferenceRequest, PlanDTO, FoodDTO, ExtraFoodDTO


class PostPlanBody(BaseModel):
    plan: Optional[PlanDTO] = Field(
        None,
        title="Plan",
        description="Plan object to be created",
    )
    preferences: Optional[FoodPreferenceRequest] = Field(
        None,
        title="Food preferences",
        description="Food preferences to be used for plan creation",
    )


class GetAllFoodsParams:
    search_name: Optional[str] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class PostFoodBody(BaseModel):
    food: FoodDTO = Field(..., description="The food item to be created")
    plan_id: int = Field(..., description="ID of the plan to link this food to")
    day_id: Optional[int] = Field(None, description="Optional day ID to pre-assign")
    meal_moment_id: Optional[int] = Field(None, description="Optional moment ID to pre-assign")

class PostExtraFoodBody(BaseModel):
    extraFood: Optional[ExtraFoodDTO] = Field(
        None,
        title="Extra Food",
        description="Extra Food object to be created",
    )

class GetExtraFoodsParams:
    user_id: str
    start_date: datetime
    end_date: datetime
    moment: Optional[str] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
