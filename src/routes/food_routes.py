from fastapi import APIRouter, status, Body

from controller.food_controller import FoodController
from models.foodPlans import FoodPlanUpdateRequest, FoodPreferenceRequest, Plan, Plans, Food, PlanAssigment, Users

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
def get_plan_by_id(aId:int) -> Plan:
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
def get_user_plan(userId:str) -> Plans:
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
    print(f"planId: {planId}")
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
def get_foods_from_user_plan(userId: str):
    return FoodController().get_foods_from_user_plan(userId)

@router.post(
    "/user/{userId}/addFood/{foodId}",
    summary="add a food to user's plan",
    status_code=status.HTTP_200_OK
)
def add_food_to_user_plan(userId: int, foodId: int) -> None:
    return FoodController().add_food_to_user_plan(userId, foodId)

@router.put(
    "/plans/{plan_id}/updateMeal",
    summary="Update a food item for a specific day and moment in plan",
    status_code=status.HTTP_200_OK
)
def update_meal_in_plan(plan_id: int, data: FoodPlanUpdateRequest):
    return FoodController().update_food_in_plan(plan_id, data.day, data.moment, data.foodId)


@router.delete(
    "/userPlan/{userId}/removeFood/{foodId}",
    summary="remove a food from user's plan",
    status_code=status.HTTP_200_OK
)
def remove_food_from_user_plan(userId: str, foodId: int) -> None:
    return FoodController().remove_food_from_user_plan(userId, foodId)

@router.post(
    "/plans/fromPreferences",
    summary="Create a new plan based on user food preferences",
    status_code=status.HTTP_201_CREATED
)
def create_plan_from_preferences(data: FoodPreferenceRequest) -> Plans:
    return FoodController().create_plan_from_preferences(data.user_id, data.preferences)
