from fastapi import APIRouter, status

from controller.food_controller import FoodController
from models.foodPlans import Plans, Food, PlanAssigment, Users

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

@router.get(
    "/userPlan/{userId}",
    summary="get the user plan",
    status_code=status.HTTP_200_OK
)
def get_user_plan(userId:int) -> Plans:
    return FoodController().get_user_plan(userId)

@router.post(
    "/user/{username}",
    summary="set a user in the db",
    status_code=status.HTTP_200_OK
)
def post_user(username:str) -> None:
    return FoodController().post_user(username)

@router.put(
    "/users/{userId}/plan",
    summary="set a plan in a user",
    status_code=status.HTTP_200_OK
)
def put_user_plan(userId: str, assigment: PlanAssigment) -> None:
    planId = assigment.plan_id
    return FoodController().put_user_plan(userId, planId)


# def post_user_plan(userId:int, planId:int) -> None:
#    return FoodController().post_user_plan(userId, planId)
#
# 2 formas de obtener las comidas de un plan: por ID de plan o ID de usuario
@router.get(
    "/plans/{planId}/foods",
    summary="Get all foods in a plan",
    status_code=status.HTTP_200_OK
)
def get_foods_from_plan(planId: int):
    return FoodController().get_foods_from_plan(planId)

@router.get(
    "/user/{userId}/foods",
    summary="Get all foods from a user's plan",
    status_code=status.HTTP_200_OK
)
def get_foods_from_user_plan(userId: int):
    return FoodController().get_foods_from_user_plan(userId)

@router.post(
    "/user/{userId}/addFood/{foodId}",
    summary="add a food to user's plan",
    status_code=status.HTTP_200_OK
)
def add_food_to_user_plan(userId: int, foodId: int) -> None:
    return FoodController().add_food_to_user_plan(userId, foodId)

@router.delete(
    "/userPlan/{userId}/removeFood/{foodId}",
    summary="remove a food from user's plan",
    status_code=status.HTTP_200_OK
)
def remove_food_from_user_plan(userId: int, foodId: int) -> None:
    return FoodController().remove_food_from_user_plan(userId, foodId)
