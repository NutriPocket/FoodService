from fastapi import APIRouter, status

from controller.food_controller import FoodController
from models.foodPlans import FoodPlans

router = APIRouter()


@router.get(
    "/plans",
    summary="get the differents plans",
    status_code=status.HTTP_200_OK
)
def get_food_plans() -> FoodPlans:
    return FoodController().get_food_plans()
