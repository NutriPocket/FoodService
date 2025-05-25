from typing import Optional
from pydantic import BaseModel, Field

from models.foodPlans import FoodPreferenceRequest, PlanDTO


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


class GetFoodByIdParams:
    with_nutrition_facts: bool = False

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
