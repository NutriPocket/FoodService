from fastapi import APIRouter, Query, status

from controller.food_controller import FoodController
from models.errors.errors import ValidationError
from models.foodPlans import Food, FoodLinkDTO, FoodTimeDTO, Plan, PlanAssignment, PlanAssignmentDTO, WeeklyPlan
from models.params import GetAllFoodsParams, PostPlanBody, PostFoodBody
from models.response import CustomResponse, ErrorDTO

router = APIRouter()


@router.get(
    "/plans",
    summary="Retrieves all the differents plans",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Plan]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_food_plans() -> CustomResponse[list[Plan]]:
    return FoodController().get_plans()


@router.get(
    "/plans/{id}",
    summary="Retrieves a specific detailed weekly plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_plan_by_id(id: int) -> CustomResponse[WeeklyPlan]:
    return FoodController().get_plan(id)


@router.post(
    "/plans",
    summary="Create a new food plan",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Plan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_plan(
    body: PostPlanBody,
    from_preferences: bool = Query(
        default=False,
        description="If true, the plan will be created from user preferences",
    )
) -> CustomResponse[Plan]:
    if from_preferences and body.preferences:
        return FoodController().create_plan_from_preferences(
            body.preferences.user_id, body.preferences.preferences, body.plan
        )

    if not body.plan:
        raise ValidationError(
            detail="If you want to create a plan from preferences, you need to provide the user_id and preferences. If you want to create a plan from scratch, you need to provide the plan title, description and objective.",
            title="Missing body or wrong body"
        )

    return FoodController().add_plan(body.plan)


@router.get(
    "/users/{user_id}/plan",
    summary="Retrieves the user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[Plan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_user_plan(user_id: str) -> CustomResponse[Plan]:
    return FoodController().get_user_plan(user_id)


@router.put(
    "/users/{user_id}/plan",
    summary="Replace the user's plan",
    description="If the user already has a plan, it will be replaced. If not, a new plan will be created.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[PlanAssignment],
            "description": "Update user's plans"
        },
        status.HTTP_201_CREATED: {
            "model": CustomResponse[PlanAssignment],
            "description": "Create user's plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def put_user_plan(assigment: PlanAssignmentDTO, user_id: str) -> CustomResponse[PlanAssignment]:
    return FoodController().put_user_plan(user_id, assigment)


# def post_user_plan(userId:int, planId:int) -> None:
#    return FoodController().post_user_plan(userId, planId)
#
# 2 formas de obtener las comidas de un plan: por ID de plan o ID de usuario
@router.get(
    "/plans/{plan_id}/foods",
    summary="Get all foods in a plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_foods_from_plan(plan_id: int) -> CustomResponse[list[Food]]:
    return FoodController().get_foods_from_plan(plan_id)


@router.get(
    "/users/{user_id}/plan/foods",
    summary="Get all foods from a user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_foods_from_user_plan(user_id: str) -> CustomResponse[list[Food]]:
    return FoodController().get_foods_from_user_plan(user_id)


@router.post(
    "/users/{user_id}/plan/foods",
    summary="Adds a new food for the user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorDTO,
            "description": "A food already exists at that moment in that day in the plan"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def add_food_to_user_plan(req: FoodLinkDTO, user_id: str) -> CustomResponse[WeeklyPlan]:
    return FoodController().add_food_to_user_plan(user_id, req)


@router.put(
    "/plans/{plan_id}/foods",
    summary="Update a food item for a specific day and moment in plan",
    description="Update a food item for a specific day and moment in plan, retrieves the updated weekly plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "Update a food from the user's plan"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Item not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def update_meal_in_plan(plan_id: int, data: FoodLinkDTO) -> CustomResponse[WeeklyPlan]:
    return FoodController().update_food_in_plan(plan_id, data)


@router.delete(
    "/users/{user_id}/plan/foods",
    summary="remove a food from user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "Remove a food from the user's plan"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def remove_food_from_user_plan(data: FoodTimeDTO, user_id: str) -> CustomResponse[WeeklyPlan]:
    return FoodController().remove_food_from_user_plan(user_id, data)


@router.get(
    "/foods/{food_id}",
    summary="Get food by id",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[Food],
            "description": "Food found"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Food not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_food_by_id(food_id: int) -> CustomResponse[Food]:
    return FoodController().get_food_by_id(food_id)


@router.get(
    "/foods",
    summary="Get all foods",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_all_foods(search_name: str = Query(None, description="Search food by name. Case insensitive. Anywhere match")) -> CustomResponse[list[Food]]:
    params = GetAllFoodsParams(search_name=search_name)

    return FoodController().get_all_foods(params)

@router.post(
    "/food",
    summary="Create a new food",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Food],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_food(body: PostFoodBody) -> CustomResponse[Food]:
    if not body.food:
        raise ValidationError(
            detail="If you want to create a food from scratch, you need to provide a long list of params...",
            title="Missing body or wrong body"
    )
    return FoodController().add_food_in_db(body.food)