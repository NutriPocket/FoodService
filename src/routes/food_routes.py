from fastapi import APIRouter, status

from controller.food_controller import FoodController
from models.foodPlans import Plans, Food, FoodPlanLink

router = APIRouter()

@router.get(
    "/plans",
    summary="get the differents plans",
    status_code=status.HTTP_200_OK
)
def get_food_plans() -> dict:
    return FoodController().get_plans()

@router.get(
    "/plans/{aId}",
    summary="get a specific plan",
    status_code=status.HTTP_200_OK
)
def get_plan_by_id(aId:int) -> Plans:
    return FoodController().get_plan(aId)

@router.post(
    "/plans/{aTitle}/{aDescription}/{aObjetive}",
    summary="post a plan in db",
    status_code=status.HTTP_200_OK
)
def post_plan(aTitle:str, aDescription:str, aObjetive:str) -> None:
    return FoodController().add_plan(aTitle, aDescription, aObjetive)
